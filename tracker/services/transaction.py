# modules/transaction.py
class Transaction:
    def __init__(self, date, category, amount, t_type):
        self.date = date
        self.category = category
        self.amount = amount
        self.t_type = t_type  # "income" or "expense"

    def to_dict(self):
        return {
            "Date": self.date,
            "Category": self.category,
            "Amount": self.amount,
            "Type": self.t_type
        }
