import sqlite3
import os
import time
from tkinter import *
from tkinter import ttk, messagebox

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("800x600")

        # Database Connection
        self.con = sqlite3.connect("ims.db")
        self.cur = self.con.cursor()
        self.root.config(bg="#333")
        self.create_table()

        # Variables
        self.var_pro = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_customer = StringVar()

        # UI Elements
        Label(self.root, bg="#333", fg="white", text="Select Product").grid(row=0, column=0, padx=10, pady=10)
        self.cmb_product = ttk.Combobox(self.root, textvariable=self.var_pro, state="readonly")
        self.cmb_product.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_product.bind("<<ComboboxSelected>>", self.update_price_qty)

        Label(self.root, bg="#333", fg="white", text="Price").grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, bg="lemon chiffon", textvariable=self.var_price, state="readonly").grid(row=1, column=1, padx=10, pady=10)

        Label(self.root, bg="#333", fg="white", text="Quantity").grid(row=2, column=0, padx=10, pady=10)
        self.cmb_qty = ttk.Combobox(self.root, textvariable=self.var_qty, state="readonly")
        self.cmb_qty.grid(row=2, column=1, padx=10, pady=10)

        Button(self.root, bg="deep sky blue", fg="#333", text="Add to Bill", command=self.add_to_bill).grid(row=3, column=0, padx=5, pady=10)
        Button(self.root, bg="light salmon", fg="#333", text="Remove Selected", command=self.remove_selected).grid(row=3, column=1, padx=5, pady=10)

        # Customer Name Input
        Label(self.root, bg="#333", fg="white", text="Customer Name").grid(row=4, column=0, padx=10, pady=10)
        Entry(self.root, bg="lemon chiffon", textvariable=self.var_customer).grid(row=4, column=1, padx=10, pady=10)

        # Bill Table (Scrollable)
        self.bill_frame = Frame(self.root)
        self.bill_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.bill_frame, columns=("Product", "Price", "Qty", "Total"), show="headings", height=6)
        self.tree.heading("Product", text="Product")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Total", text="Total Price")
        self.tree.pack()

        # Scrollbar
        scroll = Scrollbar(self.bill_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # Generate Bill Button
        Button(self.root, bg="deep sky blue", fg="#333", text="Generate Bill", command=self.generate_bill).grid(row=6, column=0, columnspan=2, pady=10)
        self.lbl_total = Label(self.root, bg="#333", fg="white", text="Total: Rs. 0")
        self.lbl_total.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_products()
        self.bill_items = []  # List to store added items

    def create_table(self):
        """Creates the product table if it doesn't exist."""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS product (
                pid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                qty INTEGER
            )
        """)
        self.con.commit()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sid INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                product_name TEXT,
                quantity INTEGER,
                price REAL,
                total_price REAL,
                date TEXT
            )
        """)
        self.con.commit()

    def load_products(self):
        """Loads products into the dropdown menu."""
        self.cur.execute("SELECT name FROM product")
        products = self.cur.fetchall()
        self.cmb_product["values"] = ["Select"] + [p[0] for p in products]
        self.cmb_product.current(0)

    def update_price_qty(self, event=None):
        """Updates price and available quantity when a product is selected."""
        product = self.var_pro.get()
        if product == "Select":
            self.var_price.set("")
            self.cmb_qty["values"] = ["Select"]
            self.cmb_qty.current(0)
            return

        self.cur.execute("SELECT price, qty FROM product WHERE name=?", (product,))
        row = self.cur.fetchone()
        if row:
            price, qty_available = row
            qty_available = int(qty_available)  # Ensure qty_available is an integer

            self.var_price.set(str(price))

            if qty_available > 0:
                self.cmb_qty["values"] = [str(i) for i in range(1, qty_available + 1)]
                self.cmb_qty.current(0)  # Set default selection
            else:
                self.cmb_qty["values"] = ["Out of stock"]
                self.cmb_qty.current(0)  # Set default selection
        else:
            self.var_price.set("")
            self.cmb_qty["values"] = ["Select"]
            self.cmb_qty.current(0)


    def add_to_bill(self):
        """Adds selected product to bill"""
        product = self.var_pro.get()
        price = self.var_price.get()
        qty = self.var_qty.get()

        if product == "Select" or not price or not qty or qty == "Select":
            messagebox.showerror("Error", "Select a valid product and quantity")
            return

        price = float(price)
        qty = int(qty)
        total_price = price * qty

        self.bill_items.append((product, price, qty, total_price))
        self.tree.insert("", "end", values=(product, price, qty, total_price))
        self.calculate_total()

    def remove_selected(self):
        """Removes selected product from bill"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an item to remove")
            return

        item_values = self.tree.item(selected_item, "values")
        self.bill_items = [item for item in self.bill_items if item != tuple(item_values)]
        self.tree.delete(selected_item)
        self.calculate_total()

    def calculate_total(self):
        """Calculates total bill amount"""
        total_amount = sum(item[3] for item in self.bill_items)
        self.lbl_total.config(text=f"Total: Rs. {total_amount:.2f}")

    def generate_bill(self):
        """Generates and saves the bill, then updates the stock in DB"""
        customer_name = self.var_customer.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Enter customer name before generating bill")
            return

        if not self.bill_items:
            messagebox.showerror("Error", "No products in bill")
            return

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for item in self.bill_items:
            product, price, qty, total_price = item
            self.cur.execute("""
                INSERT INTO sales (customer_name, product_name, quantity, price, total_price, date) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_name, product, qty, price, total_price, timestamp))
            self.cur.execute("UPDATE product SET qty = qty - ? WHERE name = ?", (qty, product))
        self.con.commit()

        messagebox.showinfo("Bill Saved", "Bill generated successfully!")
        self.bill_items.clear()
        self.tree.delete(*self.tree.get_children())  # Clear bill table
        self.calculate_total()
        self.load_products()  # Refresh available stock

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = BillingSystem(root)
    root.mainloop()
