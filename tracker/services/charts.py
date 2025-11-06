# visuals/charts.py
import pandas as pd
import matplotlib.pyplot as plt

def expense_pie_chart(df):
    expense_data = df[df["Type"] == "expense"]
    if expense_data.empty:
        print("No expense data to visualize.")
        return
    category_sum = expense_data.groupby("Category")["Amount"].sum()
    category_sum.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.show()

def income_vs_expense_bar(df):
    income = df[df["Type"] == "income"]["Amount"].sum()
    expense = df[df["Type"] == "expense"]["Amount"].sum()
    plt.bar(["Income", "Expense"], [income, expense], color=["green", "red"])
    plt.title("Income vs Expense")
    plt.show()
