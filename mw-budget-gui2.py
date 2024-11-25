import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv


class FinancialTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Debt and Savings Tracker")

        # Initialize variables
        self.total_debt = 2600
        self.remaining_debt = self.total_debt
        self.paycheck = 1000
        self.remaining_funds = self.paycheck  # Funds left after expenses for the current period
        self.savings = 0
        self.pay_period = 0
        self.expenses = []  # List to store expense data

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self.root, text="Debt and Savings Tracker", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Progress bars
        self.debt_progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.debt_progress.grid(row=1, column=0, columnspan=3, pady=5)
        ttk.Label(self.root, text="Debt Progress").grid(row=2, column=0, columnspan=3)

        self.savings_progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.savings_progress.grid(row=3, column=0, columnspan=3, pady=5)
        ttk.Label(self.root, text="Savings Progress").grid(row=4, column=0, columnspan=3)

        # Status labels
        self.debt_label = ttk.Label(self.root, text=f"Remaining Debt: ${self.remaining_debt:.2f}")
        self.debt_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.savings_label = ttk.Label(self.root, text=f"Savings: ${self.savings:.2f}")
        self.savings_label.grid(row=6, column=0, columnspan=3, pady=5)

        self.remaining_funds_label = ttk.Label(self.root, text=f"Remaining Funds: ${self.remaining_funds:.2f}")
        self.remaining_funds_label.grid(row=7, column=0, columnspan=3, pady=5)

        # Inputs for savings and expenses
        ttk.Label(self.root, text="Enter Savings:").grid(row=8, column=0, padx=10, pady=5)
        self.savings_entry = ttk.Entry(self.root)
        self.savings_entry.grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Log Expense:").grid(row=9, column=0, padx=10, pady=5)
        self.expense_entry = ttk.Entry(self.root)
        self.expense_entry.grid(row=9, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Description:").grid(row=9, column=2, padx=10, pady=5)
        self.expense_description = ttk.Entry(self.root)
        self.expense_description.grid(row=9, column=3, padx=10, pady=5)

        # Buttons
        self.save_button = ttk.Button(self.root, text="Save", command=self.save_savings)
        self.save_button.grid(row=10, column=0, pady=5)

        self.expense_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.expense_button.grid(row=10, column=1, pady=5)

        self.next_button = ttk.Button(self.root, text="Next Pay Period", command=self.update_tracker)
        self.next_button.grid(row=11, column=0, columnspan=3, pady=10)

        self.export_button = ttk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=11, column=2, pady=10)

        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=12, column=0, columnspan=3, pady=10)

        self.plan_button = ttk.Button(self.root, text = "Fastest Payback Plan", command=self.calculate_fastest_route)
        self.plan_button.grid(row = 11, column=3, pady=10)

        # Expense report table
        self.expense_table = ttk.Treeview(self.root, columns=("Date", "Description", "Amount"), show="headings", height=10)
        self.expense_table.grid(row=13, column=0, columnspan=3, pady=10)
        self.expense_table.heading("Date", text="Date")
        self.expense_table.heading("Description", text="Description")
        self.expense_table.heading("Amount", text="Amount")
        self.expense_table.column("Date", width=100)
        self.expense_table.column("Description", width=200)
        self.expense_table.column("Amount", width=100)

    def save_savings(self):
        try:
            savings = float(self.savings_entry.get())
            if savings > self.remaining_funds:
                messagebox.showerror("Error", "Savings amount exceeds remaining funds!")
            else:
                self.savings += savings
                self.remaining_funds -= savings
                self.savings_label.config(text=f"Savings: ${self.savings:.2f}")
                self.remaining_funds_label.config(text=f"Remaining Funds: ${self.remaining_funds:.2f}")
                self.savings_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for savings.")

    def add_expense(self):
        try:
            expense = float(self.expense_entry.get())
            description = self.expense_description.get()
            if expense > self.remaining_funds:
                messagebox.showerror("Error", "Expense exceeds remaining funds!")
            elif not description:
                messagebox.showerror("Error", "Please provide a description for the expense.")
            else:
                self.remaining_funds -= expense
                self.remaining_funds_label.config(text=f"Remaining Funds: ${self.remaining_funds:.2f}")
                self.expense_entry.delete(0, tk.END)
                self.expense_description.delete(0, tk.END)
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.expenses.append({"Date": date, "Description": description, "Amount": expense})
                self.expense_table.insert("", tk.END, values=(date, description, f"${expense:.2f}"))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the expense.")

    def update_tracker(self):
        if self.remaining_debt > 0:
            self.pay_period += 1
            debt_payment = min(self.remaining_funds, self.remaining_debt)
            self.remaining_debt -= debt_payment
            self.remaining_funds = self.paycheck
            self.debt_progress["value"] = (1 - self.remaining_debt / self.total_debt) * 100
            self.savings_progress["value"] = (self.savings / self.total_debt) * 100
            self.debt_label.config(text=f"Remaining Debt: ${self.remaining_debt:.2f}")
            self.remaining_funds_label.config(text=f"Remaining Funds: ${self.remaining_funds:.2f}")
        if self.remaining_debt <= 0:
            self.next_button.config(state="disabled")
            self.debt_label.config(text="Debt Paid Off!")
            ttk.Label(self.root, text=f"Debt cleared in {self.pay_period} pay periods!").grid(row=14, column=0, columnspan=3, pady=10)

    def export_to_csv(self):
        save_path = "C:/Users/williams-martin/Documents/expenses_report.csv"
        with open(save_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Description", "Amount"])
            writer.writeheader()
            writer.writerows(self.expenses)
        messagebox.showinfo("Export Successful", "Expenses exported to expenses_report.csv")

    def calculate_fastest_route(self):
        debt = self.remaining_debt
        funds = self.paycheck
        savings_goal = 300  # Minimum savings per pay period (can be adjusted)
        pay_periods = []

        total_savings = self.savings
        pay_period_count = 0

        while debt > 0:
            pay_period_count += 1

            # Calculate payment toward debt and savings
            savings = savings_goal
            debt_payment = min(funds - savings, debt)

            # Update debt and total savings
            debt -= debt_payment
            total_savings += savings

            # Log this pay period's data
            pay_periods.append({
                "Pay Period": pay_period_count,
                "Debt Payment": debt_payment,
                "Savings": savings,
                "Remaining Debt": debt,
                "Total Savings": total_savings,
            })

        # Display the breakdown
        self.display_fastest_route(pay_periods)

    def display_fastest_route(self, pay_periods):
        # Create a new window to show the payback plan
        plan_window = tk.Toplevel(self.root)
        plan_window.title("Fastest Payback Plan")

        ttk.Label(plan_window, text="Fastest Payback Plan", font=("Arial", 14)).grid(row=0, column=0, columnspan=5, pady=10)

        # Table headings
        headings = ["Pay Period", "Debt Payment", "Savings", "Remaining Debt", "Total Savings"]
        for col, heading in enumerate(headings):
            ttk.Label(plan_window, text=heading, font=("Arial", 12, "bold")).grid(row=1, column=col, padx=5)

        # Fill in the table
        for row, data in enumerate(pay_periods, start=2):
            ttk.Label(plan_window, text=data["Pay Period"]).grid(row=row, column=0)
            ttk.Label(plan_window, text=f"${data['Debt Payment']:.2f}").grid(row=row, column=1)
            ttk.Label(plan_window, text=f"${data['Savings']:.2f}").grid(row=row, column=2)
            ttk.Label(plan_window, text=f"${data['Remaining Debt']:.2f}").grid(row=row, column=3)
            ttk.Label(plan_window, text=f"${data['Total Savings']:.2f}").grid(row=row, column=4)

        ttk.Button(plan_window, text="Close", command=plan_window.destroy).grid(row=row + 1, column=0, columnspan=5, pady=10)



# Run the app
root = tk.Tk()
app = FinancialTrackerApp(root)
root.mainloop()

