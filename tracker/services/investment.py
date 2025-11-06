# modules/investment.py
import pandas as pd

class InvestmentAnalyzer:
    def __init__(self, df):
        self.df = df[df["Category"].str.lower() == "investment"]

    def analyze(self):
        if self.df.empty:
            print("\nNo investment data found.")
            return

        total_investment = self.df["Amount"].sum()
        print(f"\n💼 Total Invested Amount: ₹{total_investment}")

        monthly_investment = self.df.groupby("Date")["Amount"].sum()
        print("\nMonthly Investment Data:")
        print(monthly_investment)
        return monthly_investment
