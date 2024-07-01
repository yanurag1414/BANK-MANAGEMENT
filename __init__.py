import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("400x600")

        self.connect_to_database()
        self.create_widgets()

    def connect_to_database(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lavanu#1",
            database="bank_management"
        )
        self.cursor = self.conn.cursor()

    def create_widgets(self):
        # Title
        self.title_label = ttk.Label(self.root, text="Bank Management System", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Frame for Adding Customer
        self.add_frame = ttk.LabelFrame(self.root, text="Add Customer", padding=(10, 5))
        self.add_frame.pack(pady=10, fill="x", padx=20)

        self.name_label = ttk.Label(self.add_frame, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.balance_label = ttk.Label(self.add_frame, text="Initial Balance:")
        self.balance_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.balance_entry = ttk.Entry(self.add_frame)
        self.balance_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Customer", command=self.add_customer)
        self.add_button.grid(row=2, columnspan=2, pady=10)

        # Frame for Viewing Customers
        self.view_frame = ttk.LabelFrame(self.root, text="View Customers", padding=(10, 5))
        self.view_frame.pack(pady=10, fill="x", padx=20)

        self.view_button = ttk.Button(self.view_frame, text="View Customers", command=self.view_customers)
        self.view_button.pack(pady=10)

        # Frame for Deposit Money
        self.deposit_frame = ttk.LabelFrame(self.root, text="Deposit Money", padding=(10, 5))
        self.deposit_frame.pack(pady=10, fill="x", padx=20)

        self.deposit_id_label = ttk.Label(self.deposit_frame, text="Customer ID:")
        self.deposit_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.deposit_id_entry = ttk.Entry(self.deposit_frame)
        self.deposit_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.deposit_amount_label = ttk.Label(self.deposit_frame, text="Deposit Amount:")
        self.deposit_amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.deposit_amount_entry = ttk.Entry(self.deposit_frame)
        self.deposit_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.deposit_button = ttk.Button(self.deposit_frame, text="Deposit", command=self.deposit_money)
        self.deposit_button.grid(row=2, columnspan=2, pady=10)

        # Frame for Withdraw Money
        self.withdraw_frame = ttk.LabelFrame(self.root, text="Withdraw Money", padding=(10, 5))
        self.withdraw_frame.pack(pady=10, fill="x", padx=20)

        self.withdraw_id_label = ttk.Label(self.withdraw_frame, text="Customer ID:")
        self.withdraw_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.withdraw_id_entry = ttk.Entry(self.withdraw_frame)
        self.withdraw_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.withdraw_amount_label = ttk.Label(self.withdraw_frame, text="Withdraw Amount:")
        self.withdraw_amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.withdraw_amount_entry = ttk.Entry(self.withdraw_frame)
        self.withdraw_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.withdraw_button = ttk.Button(self.withdraw_frame, text="Withdraw", command=self.withdraw_money)
        self.withdraw_button.grid(row=2, columnspan=2, pady=10)

    def add_customer(self):
        name = self.name_entry.get()
        balance = self.balance_entry.get()

        if name and balance.isdigit():
            query = "INSERT INTO customers (name, balance) VALUES (%s, %s)"
            self.cursor.execute(query, (name, float(balance)))
            self.conn.commit()
            messagebox.showinfo("Success", f"Customer '{name}' added with balance {balance}.")
        else:
            messagebox.showerror("Error", "Please enter a valid name and balance.")

    def view_customers(self):
        query = "SELECT * FROM customers"
        self.cursor.execute(query)
        customers = self.cursor.fetchall()

        customers_info = "Customers:\n"
        for customer in customers:
            customers_info += f"ID: {customer[0]}, Name: {customer[1]}, Balance: {customer[2]}\n"

        messagebox.showinfo("Customers", customers_info)

    def deposit_money(self):
        customer_id = self.deposit_id_entry.get()
        amount = self.deposit_amount_entry.get()

        if customer_id.isdigit() and amount.isdigit():
            query = "UPDATE customers SET balance = balance + %s WHERE id = %s"
            self.cursor.execute(query, (float(amount), int(customer_id)))
            self.conn.commit()
            if self.cursor.rowcount:
                messagebox.showinfo("Success", f"Deposited {amount} to ID {customer_id}.")
            else:
                messagebox.showerror("Error", "Customer ID not found.")
        else:
            messagebox.showerror("Error", "Invalid customer ID or amount.")

    def withdraw_money(self):
        customer_id = self.withdraw_id_entry.get()
        amount = self.withdraw_amount_entry.get()

        if customer_id.isdigit() and amount.isdigit():
            query = "SELECT balance FROM customers WHERE id = %s"
            self.cursor.execute(query, (int(customer_id),))
            result = self.cursor.fetchone()

            if result and result[0] >= float(amount):
                query = "UPDATE customers SET balance = balance - %s WHERE id = %s"
                self.cursor.execute(query, (float(amount), int(customer_id)))
                self.conn.commit()
                messagebox.showinfo("Success", f"Withdrew {amount} from ID {customer_id}.")
            elif result:
                messagebox.showerror("Error", "Insufficient funds.")
            else:
                messagebox.showerror("Error", "Customer ID not found.")
        else:
            messagebox.showerror("Error", "Invalid customer ID or amount.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()
