# modules/expense_tracker.py
import csv
import os

try:
    import pandas as pd  # type: ignore
except ImportError:
    print("Please install pandas using: pip install pandas")
    raise

REQUIRED_FIELDS = ["Date", "Category", "Amount", "Type"]

class ExpenseTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        # ensure data folder exists
        folder = os.path.dirname(file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        # create file with header if not exists or if invalid
        if not os.path.exists(file_path):
            self._create_empty_file()
        else:
            # check validity of existing file, recreate if badly formatted
            if not self._file_has_valid_header():
                print("⚠️ Existing CSV missing required headers — recreating file with correct headers.")
                self._create_empty_file()

    def _create_empty_file(self):
        with open(self.file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_FIELDS)
            writer.writeheader()

    def _file_has_valid_header(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header is None:
                    return False
                # normalize header names
                header_norm = [h.strip().lower() for h in header]
                required_norm = [h.lower() for h in REQUIRED_FIELDS]
                return set(required_norm).issubset(set(header_norm))
        except Exception:
            return False

    def add_transaction(self, transaction):
        # ensure Amount is numeric and Type is normalized before writing
        record = transaction.to_dict()
        # normalize Type to lowercase
        record["Type"] = str(record.get("Type", "")).strip().lower()
        # ensure Amount is numeric-like string
        try:
            record["Amount"] = float(record.get("Amount", 0))
        except (ValueError, TypeError):
            # fallback: write 0.0 and warn
            print("⚠️ Invalid amount provided, saved as 0.0")
            record["Amount"] = 0.0

        with open(self.file_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_FIELDS)
            writer.writerow({
                "Date": record.get("Date", ""),
                "Category": record.get("Category", ""),
                "Amount": record.get("Amount", 0),
                "Type": record.get("Type", "")
            })

    def _read_dataframe(self):
        # read csv, normalize columns, coerce Amount to numeric
        try:
            df = pd.read_csv(self.file_path, dtype=str)  # read as strings first
        except Exception as e:
            print("⚠️ Unable to read CSV:", e)
            return pd.DataFrame(columns=REQUIRED_FIELDS)

        if df.empty:
            # ensure correct columns exist
            df = pd.DataFrame(columns=REQUIRED_FIELDS)
            return df

        # normalize column names to expected casing
        col_map = {}
        for c in df.columns:
            for req in REQUIRED_FIELDS:
                if c.strip().lower() == req.lower():
                    col_map[c] = req
                    break
        df = df.rename(columns=col_map)

        # add missing required columns with defaults
        for req in REQUIRED_FIELDS:
            if req not in df.columns:
                df[req] = ""

        # coerce Amount to numeric (float). invalid -> 0
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)

        # normalize Type values to lowercase strings
        df["Type"] = df["Type"].astype(str).str.strip().str.lower()

        # strip whitespace from Category and Date
        df["Category"] = df["Category"].astype(str).str.strip()
        df["Date"] = df["Date"].astype(str).str.strip()

        return df

    def view_summary(self):
        df = self._read_dataframe()

        # debug: if dataframe columns aren't present show helpful message
        if df.empty or not set(REQUIRED_FIELDS).issubset(set(df.columns)):
            print("⚠️ No valid data available. Add a transaction first.")
            return df

        # compute totals
        total_income = df[df["Type"] == "income"]["Amount"].sum()
        total_expense = df[df["Type"] == "expense"]["Amount"].sum()
        balance = total_income - total_expense

        # print summary
        print(f"\n💰 Total Income: ₹{total_income:.2f}")
        print(f"💸 Total Expense: ₹{total_expense:.2f}")
        print(f"📈 Savings: ₹{balance:.2f}")

        # top expense category (safely)
        expense_df = df[df["Type"] == "expense"]
        if not expense_df.empty:
            # groupby Category, sum Amount
            cat_sum = expense_df.groupby("Category", dropna=False)["Amount"].sum()
            # if all categories are empty string, handle gracefully
            if not cat_sum.empty and cat_sum.sum() > 0:
                top_category = cat_sum.idxmax()
                top_value = cat_sum.max()
                print(f"🏆 Highest Expense Category: {top_category} (₹{top_value:.2f})")
            else:
                print("No expense amounts recorded yet.")
        else:
            print("No expense records yet.")

        return df
