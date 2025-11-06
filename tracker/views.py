from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import os
import pandas as pd

from .services.expense_tracker import ExpenseTracker
from .services.transaction import Transaction
from .services.investment import InvestmentAnalyzer

# ✅ CSV file path
DATA_FILE = os.path.join(settings.BASE_DIR, "data", "transactions.csv")

# Ensure file exists and has valid headers
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Date", "Category", "Amount", "Type"]).to_csv(DATA_FILE, index=False)


# -----------------------------------------------
# 🏠 DASHBOARD VIEW
# -----------------------------------------------
def home(request):
    """Main dashboard page with filters, search, and delete support."""
    tracker = ExpenseTracker(DATA_FILE)
    df = tracker.view_summary()

    # Remove duplicate headers and invalid rows
    if not df.empty and "Date" in df["Date"].values:
        df = df[df["Date"] != "Date"]

    # Filters
    month_filter = request.GET.get("month")
    category_filter = request.GET.get("category")
    search_query = request.GET.get("search", "").strip().lower()

    if not df.empty:
        # Apply filters
        if month_filter:
            df = df[df["Date"].astype(str).str.startswith(month_filter)]
        if category_filter and category_filter != "All":
            df = df[df["Category"] == category_filter]
        if search_query:
            df = df[df.apply(lambda x: search_query in str(x).lower(), axis=1)]

    # Prepare summary
    summary = {
        "income": 0,
        "expense": 0,
        "balance": 0,
        "top_category": None,
        "top_value": 0,
    }

    if not df.empty:
        summary["income"] = float(df[df["Type"] == "income"]["Amount"].sum())
        summary["expense"] = float(df[df["Type"] == "expense"]["Amount"].sum())
        summary["balance"] = summary["income"] - summary["expense"]

        expense_df = df[df["Type"] == "expense"]
        if not expense_df.empty:
            grouped = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            if not grouped.empty:
                summary["top_category"] = grouped.index[0]
                summary["top_value"] = grouped.iloc[0]

    # Dropdown filters
    all_months = sorted(df["Date"].astype(str).str[:7].unique()) if not df.empty else []
    all_categories = sorted(df["Category"].unique()) if not df.empty else []

    # Show last 10 filtered transactions
    recent = df.sort_values("Date", ascending=False).head(10).reset_index(drop=True).to_dict("records") if not df.empty else []

    return render(request, "tracker/dashboard.html", {
        "summary": summary,
        "recent": recent,
        "months": all_months,
        "categories": all_categories,
        "selected_month": month_filter or "",
        "selected_category": category_filter or "All",
        "search_query": search_query,
    })


# -----------------------------------------------
# ➕ ADD TRANSACTION
# -----------------------------------------------
def add_transaction(request):
    """Add a new transaction (income/expense/investment)."""
    if request.method == "POST":
        date = request.POST.get("date")
        category = request.POST.get("category")
        amount = float(request.POST.get("amount"))
        t_type = request.POST.get("t_type")

        trans = Transaction(date, category, amount, t_type)
        tracker = ExpenseTracker(DATA_FILE)
        tracker.add_transaction(trans)

        return redirect("home")

    return render(request, "tracker/add_transaction.html")

def add_investment(request):
    """Add a new investment (auto type: investment)."""
    if request.method == "POST":
        date = request.POST.get("date")
        category = request.POST.get("category")
        amount = float(request.POST.get("amount"))
        t_type = "investment"  # auto-set

        trans = Transaction(date, category, amount, t_type)
        tracker = ExpenseTracker(DATA_FILE)
        tracker.add_transaction(trans)

        return redirect("manage_investments")

    return render(request, "tracker/add_investment.html")

# -----------------------------------------------
# 💹 INVESTMENT ANALYZER
# -----------------------------------------------
def analyze_investment(request):
    """Analyze and visualize investment performance."""
    tracker = ExpenseTracker(DATA_FILE)
    df = tracker.view_summary()

    if df.empty:
        return render(request, "tracker/investment.html", {"error": "No transactions found."})

    # Detect investment transactions flexibly
    inv_df = df[df["Category"].str.lower().str.contains("invest|sip|mf|fund|stock", na=False)]

    if inv_df.empty:
        return render(request, "tracker/investment.html", {"error": "No investment data available."})

    inv_df["Date"] = pd.to_datetime(inv_df["Date"], errors="coerce")
    inv_df = inv_df.dropna(subset=["Date"])
    inv_df["Month"] = inv_df["Date"].dt.strftime("%Y-%m")

    monthly_summary = inv_df.groupby("Month")["Amount"].sum().reset_index().sort_values("Month")
    labels = monthly_summary["Month"].tolist()
    data = monthly_summary["Amount"].tolist()

    total_invested = float(inv_df["Amount"].sum())
    avg_monthly = round(total_invested / len(monthly_summary), 2) if len(monthly_summary) > 0 else 0

    cat_breakdown = inv_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index()
    cat_labels = cat_breakdown["Category"].tolist()
    cat_data = cat_breakdown["Amount"].tolist()

    recent_investments = inv_df.sort_values("Date", ascending=False).head(10).to_dict("records")

    context = {
        "total_invested": total_invested,
        "avg_monthly": avg_monthly,
        "labels": labels,
        "data": data,
        "cat_labels": cat_labels,
        "cat_data": cat_data,
        "recent_investments": recent_investments,
    }

    return render(request, "tracker/investment.html", context)


# -----------------------------------------------
# 🧾 MANAGE INVESTMENTS PAGE
# -----------------------------------------------
def manage_investments(request):
    """View and manage all investment transactions."""
    df = pd.read_csv(DATA_FILE)

    if df.empty or not any(df["Category"].str.lower().str.contains("invest")):
        return render(request, "tracker/manage_investments.html", {"error": "No investment records found."})

    inv_df = df[df["Category"].str.lower().str.contains("invest")].copy().reset_index(drop=True)
    inv_df["id"] = inv_df.index

    return render(request, "tracker/manage_investments.html", {"investments": inv_df.to_dict("records")})


# -----------------------------------------------
# ✏️ EDIT & DELETE INVESTMENT
# -----------------------------------------------
def edit_investment(request, row_id):
    """Edit an existing investment by its row ID."""
    df = pd.read_csv(DATA_FILE).reset_index(drop=True)

    if row_id >= len(df):
        return redirect("manage_investments")

    if request.method == "POST":
        df.loc[row_id, "Date"] = request.POST.get("date")
        df.loc[row_id, "Category"] = request.POST.get("category")
        df.loc[row_id, "Amount"] = float(request.POST.get("amount"))
        df.to_csv(DATA_FILE, index=False)
        return redirect("manage_investments")

    investment = df.loc[row_id]
    return render(request, "tracker/edit_investment.html", {"investment": investment, "row_id": row_id})


def delete_investment(request, row_id):
    """Delete only the specific investment safely."""
    df = pd.read_csv(DATA_FILE).reset_index(drop=True)
    if 0 <= row_id < len(df):
        df = df.drop(row_id).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
    return redirect("manage_investments")


# -----------------------------------------------
# ❌ DELETE SPECIFIC TRANSACTION
# -----------------------------------------------
def delete_transaction(request, row_id):
    """Safely delete only one transaction."""
    df = pd.read_csv(DATA_FILE).reset_index(drop=True)
    if 0 <= row_id < len(df):
        df = df.drop(row_id).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
    return redirect("home")


# -----------------------------------------------
# 📊 CHART DATA
# -----------------------------------------------
def expense_chart_data(request):
    """Return expense data by category for Chart.js."""
    tracker = ExpenseTracker(DATA_FILE)
    df = tracker.view_summary()

    expense_df = df[df["Type"] == "expense"] if not df.empty else pd.DataFrame()

    if expense_df.empty:
        return JsonResponse({"labels": [], "data": []})

    grouped = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    labels = grouped.index.tolist()
    data = grouped.values.tolist()

    return JsonResponse({"labels": labels, "data": data})
