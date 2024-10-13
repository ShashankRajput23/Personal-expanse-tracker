import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Setup SQLite database
def create_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        category TEXT,
        description TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to add expense
def add_expense():
    date = entry_date.get()
    amount = entry_amount.get()
    category = entry_category.get()
    description = entry_description.get()

    if not date or not amount or not category:
        messagebox.showerror("Input Error", "Please fill all fields")
        return

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)',
                   (date, amount, category, description))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully!")
    clear_entries()

# Function to view expenses
def view_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    # Display expenses in a new window
    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")
    text_area = tk.Text(view_window)
    text_area.pack(fill=tk.BOTH, expand=1)

    for expense in expenses:
        text_area.insert(tk.END, f"ID: {expense[0]}, Date: {expense[1]}, Amount: {expense[2]}, "
                                 f"Category: {expense[3]}, Description: {expense[4]}\n")

# Function to generate report by category
def report_by_category():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    report = cursor.fetchall()
    conn.close()

    # Display report in a new window
    report_window = tk.Toplevel(root)
    report_window.title("Report by Category")
    text_area = tk.Text(report_window)
    text_area.pack(fill=tk.BOTH, expand=1)

    for category, total in report:
        text_area.insert(tk.END, f"Category: {category}, Total: {total}\n")

# Function to visualize expenses by category
def visualize_expenses_by_category():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()

    if data:
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses available for visualization.")

# Function to clear input fields
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# Initialize the database
create_db()

# Setup the Tkinter window
root = tk.Tk()
root.title("Personal Expense Tracker")

# Date input
label_date = tk.Label(root, text="Date (YYYY-MM-DD):")
label_date.grid(row=0, column=0, padx=10, pady=10)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=10, pady=10)

# Amount input
label_amount = tk.Label(root, text="Amount:")
label_amount.grid(row=1, column=0, padx=10, pady=10)
entry_amount = tk.Entry(root)
entry_amount.grid(row=1, column=1, padx=10, pady=10)

# Category input
label_category = tk.Label(root, text="Category:")
label_category.grid(row=2, column=0, padx=10, pady=10)
entry_category = tk.Entry(root)
entry_category.grid(row=2, column=1, padx=10, pady=10)

# Description input
label_description = tk.Label(root, text="Description:")
label_description.grid(row=3, column=0, padx=10, pady=10)
entry_description = tk.Entry(root)
entry_description.grid(row=3, column=1, padx=10, pady=10)

# Add expense button
btn_add_expense = tk.Button(root, text="Add Expense", command=add_expense)
btn_add_expense.grid(row=4, column=0, columnspan=2, pady=10)

# View expenses button
btn_view_expenses = tk.Button(root, text="View Expenses", command=view_expenses)
btn_view_expenses.grid(row=5, column=0, columnspan=2, pady=10)

# Generate report button
btn_report_category = tk.Button(root, text="Report by Category", command=report_by_category)
btn_report_category.grid(row=6, column=0, columnspan=2, pady=10)

# Visualize expenses button
btn_visualize = tk.Button(root, text="Visualize Expenses", command=visualize_expenses_by_category)
btn_visualize.grid(row=7, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop
root.mainloop()
