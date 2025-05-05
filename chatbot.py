import sqlite3
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime, timedelta
import threading

class SupplierBot:
    def __init__(self):
        self.chatbot = ChatBot('ChatBot')
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer.train("chatterbot.corpus.english")
    
    # ========== DB Functions for Suppliers ==========    
    def get_all_suppliers(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier")
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No suppliers found."
        return "\n".join([f"Invoice: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Description: {row[3]}" for row in rows])

    def get_supplier_by_name(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier WHERE name LIKE ?", ('%' + name + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"Invoice: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Description: {row[3]}"
        return "Supplier not found."

    def get_supplier_by_contact(self, contact):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier WHERE contact LIKE ?", ('%' + contact + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"Invoice: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Description: {row[3]}"
        return "Supplier not found."

    def get_supplier_by_description(self, desc):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier WHERE description LIKE ?", ('%' + desc + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"Invoice: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Description: {row[3]}"
        return "Supplier not found."

    def get_supplier_by_invoice(self, invoice):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier WHERE invoice = ?", (invoice,))
        row = cur.fetchone()
        con.close()
        if row:
            return f"Invoice: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Description: {row[3]}"
        return "Supplier not found."
    # ========== DB Functions for categorys ==========    
    def get_all_category(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM category")
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No categorys found."
        return "\n".join([f"ID: {row[0]}, Category: {row[1]}" for row in rows])

    def get_category_by_id(self, cid):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM category WHERE cid = ?", (cid,))
        row = cur.fetchone()
        con.close()
        return row if row else "category not found."

    def get_category_by_name(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM category WHERE LOWER(name) = ?", (name.lower(),))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "category not found."
        return "\n".join([f"ID: {row[0]}, Category: {row[1]}" for row in rows])

    # ========== DB Functions for Products ==========    
    def get_all_products(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No products found."
        return "\n".join([f"ID: {row[0]}, Category: {row[1]}, Supplier: {row[2]}, Name: {row[3]}, Price: {row[4]}, Qty: {row[5]}, Status: {row[6]}" for row in rows])

    def get_product_by_id(self, pid):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE pid = ?", (pid,))
        row = cur.fetchone()
        con.close()
        return row if row else "Product not found."

    def get_product_by_name(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE LOWER(name) = ?", (name.lower(),))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "Product not found."
        return "\n".join([f"ID: {row[0]}, Category: {row[1]}, Supplier: {row[2]}, Name: {row[3]}, Price: {row[4]}, Qty: {row[5]}, Status: {row[6]}" for row in rows])

    def get_product_by_category(self, category):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE Category LIKE ?", ('%' + category + '%',))
        row = cur.fetchone()
        con.close()
        return row if row else "Product not found."

    def get_product_by_supplier(self, supplier):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE LOWER(supplier) = ?", (supplier.lower(),))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "Product not found."
        return "\n".join([f"ID: {row[0]}, Category: {row[1]}, Supplier: {row[2]}, Name: {row[3]}, Price: {row[4]}, Qty: {row[5]}, Status: {row[6]}" for row in rows])

    def get_product_by_status(self, status):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE status LIKE ?", ('%' + status + '%',))
        row = cur.fetchone()
        con.close()
        return row if row else "Product not found."

    def get_product_by_qty(self, condition, value):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        query = f"SELECT * FROM product WHERE CAST(qty AS INTEGER) {condition} ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        con.close()
        return rows if rows else "No product found with that quantity."

    def get_product_by_price(self, condition, value):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        query = f"SELECT * FROM product WHERE CAST(price AS REAL) {condition} ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        con.close()
        return rows if rows else "No product found with that price."
    # =========== db functions for employees=====
    def get_all_employees(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No employees found."
        return "\n".join([f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Contact: {row[3]}, Gender: {row[4]}, DOB: {row[5]}, DOJ: {row[6]}, Salary: {row[10]}" for row in rows])

    # Get employee by name
    def get_employee_by_name(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employee WHERE name LIKE ?", ('%' + name + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Contact: {row[3]}, Gender: {row[4]}, DOB: {row[5]}, DOJ: {row[6]}, Salary: {row[10]}"
        return "Employee not found."

    # Get employee by email
    def get_employee_by_email(self, email):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employee WHERE email LIKE ?", ('%' + email + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Contact: {row[3]}, Gender: {row[4]}, DOB: {row[5]}, DOJ: {row[6]}, Salary: {row[10]}"
        return "Employee not found."

    # Get employee by contact number
    def get_employee_by_contact(self, contact):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employee WHERE contact LIKE ?", ('%' + contact + '%',))
        row = cur.fetchone()
        con.close()
        if row:
            return f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Contact: {row[3]}, Gender: {row[4]}, DOB: {row[5]}, DOJ: {row[6]}, Salary: {row[10]}"
        return "Employee not found."

    # Get employee by ID
    def get_employee_by_id(self, eid):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employee WHERE eid = ?", (eid,))
        row = cur.fetchone()
        con.close()
        if row:
            return f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Contact: {row[3]}, Gender: {row[4]}, DOB: {row[5]}, DOJ: {row[6]}, Salary: {row[10]}"
        return "Employee not found."
     # ========== DB Functions for sales ==========    
    def get_all_sales(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM sales")
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sales found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    # def get_sale_by_id(self, sid):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()
    #     cur.execute("SELECT * FROM sales WHERE sid = ?", (sid,))
    #     row = cur.fetchone()
    #     con.close()
    #     return row if row else "sale not found."

    # def get_total_sales_on_date(self, date_keyword):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     if date_keyword == "today":
    #         date_obj = datetime.today().date()
    #     elif date_keyword == "yesterday":
    #         date_obj = (datetime.today() - timedelta(days=1)).date()
    #     else:
    #         return "Invalid date keyword."

    #     cur.execute("SELECT SUM(total_price) FROM sales WHERE date = ?", (str(date_obj),))
    #     total = cur.fetchone()[0]
    #     con.close()

    #     return f"Total sales on {date_obj}: {total}" if total else "No sales found on that date."
    # def get_total_sales_between_dates(self, start_date, end_date):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     cur.execute("SELECT SUM(total_price) FROM sales WHERE date BETWEEN ? AND ?", (start_date, end_date))
    #     total = cur.fetchone()[0]
    #     con.close()

    #     return f"Total sales from {start_date} to {end_date}: {total}" if total else "No sales in that range."

    # def get_sale_by_name(self, name):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()
    #     cur.execute("SELECT * FROM sales WHERE LOWER(customer_name) = ?", (name.lower(),))
    #     rows = cur.fetchall()
    #     con.close()
    #     if not rows:
    #         return "sale not found."
    #     return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])
    # def get_sale_by_product(self, name):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()
    #     cur.execute("SELECT * FROM sales WHERE LOWER(product_name) = ?", (name.lower(),))
    #     rows = cur.fetchall()
    #     con.close()
    #     if not rows:
    #         return "sale not found."
    #     return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])
    # def get_sale_by_category(self, category):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     cur.execute("SELECT name FROM product WHERE category LIKE ?", ('%' + category + '%',))
    #     products = cur.fetchall()

    #     if not products:
    #         con.close()
    #         return "No products found in this category."

    #     product_names = [product[0] for product in products]
    #     placeholders = ','.join(['?'] * len(product_names))
    #     cur.execute(f"SELECT * FROM sales WHERE product_name IN ({placeholders})", product_names)
    #     sales = cur.fetchall()
    #     con.close()

    #     return sales if sales else "No sales found for this category."

    # def get_sale_by_qty(self, condition, value):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()
    #     query = f"SELECT * FROM sales WHERE CAST(quantity AS INTEGER) {condition} ?"
    #     cur.execute(query, (value,))
    #     rows = cur.fetchall()
    #     con.close()
    #     return rows if rows else "No sale found with that quantity."

    # def get_sale_by_price(self, condition, value):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()
    #     query = f"SELECT * FROM sales WHERE CAST(price AS REAL) {condition} ?"
    #     cur.execute(query, (value,))
    #     rows = cur.fetchall()
    #     con.close()
    #     return rows if rows else "No sale found with that price."
    # def get_most_sold_product(self):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     cur.execute("SELECT product, SUM(qty) as total_qty FROM sales GROUP BY product ORDER BY total_qty DESC LIMIT 1")
    #     row = cur.fetchone()
    #     con.close()

    #     return f"Most sold product: {row[0]} (Quantity: {row[1]})" if row else "No sales data available."
    # def get_revenue_by_category(self):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     cur.execute("SELECT category, SUM(total_price) FROM sales GROUP BY category")
    #     rows = cur.fetchall()
    #     con.close()

    #     if not rows:
    #         return "No sales data found."
    #     return "\n".join([f"{row[0]}: ₹{row[1]}" for row in rows])
    # def get_products_sold_more_than(self, count):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     cur.execute("SELECT product, SUM(qty) as total_qty FROM sales GROUP BY product HAVING total_qty > ?", (count,))
    #     rows = cur.fetchall()
    #     con.close()

    #     if not rows:
    #         return f"No products sold more than {count} times."
    #     return "\n".join([f"{row[0]}: {row[1]} units sold" for row in rows])

    # def get_sales_by_category_and_date(self, category, condition_raw, date_str):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     today = datetime.today()
    #     yesterday = today - timedelta(days=1)

    #     try:
    #         # Normalize keywords
    #         if "today" in date_str.lower():
    #             date_obj = today.date()
    #         elif "yesterday" in date_str.lower():
    #             date_obj = yesterday.date()
    #         else:
    #             # Try to parse date in format YYYY-MM-DD
    #             date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d').date()

    #         condition = "="
    #         if condition_raw in [">", "<", ">=", "<=", "="]:
    #             condition = condition_raw

    #         # Query sales and product data based on category and date condition
    #         query = f"""
    #         SELECT s.sid, s.customer_name, s.product_name, s.quantity, s.price, s.total_price, s.date
    #         FROM sales s
    #         JOIN product p ON s.product_name = p.name
    #         WHERE p.Category = ? AND s.date {condition} ?
    #         """
    #         print(f"Executing query: {query} with parameters: ({category}, {str(date_obj)})")  # Log the query
    #         cur.execute(query, (category, str(date_obj)))
    #         rows = cur.fetchall()
    #         con.close()

    #         if not rows:
    #             return "No sales found for that category on the specified date."

    #         return "\n".join([
    #             f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}"
    #             for row in rows
    #         ])
    #     except ValueError:
    #         con.close()
    #         return "Invalid date format. Use YYYY-MM-DD or 'today'/'yesterday'."


    # def get_customers_by_product(self, product_name):
    #     con = sqlite3.connect('ims.db')
    #     cur = con.cursor()

    #     query = "SELECT DISTINCT customer_name FROM sales WHERE product_name = ?"
    #     print(f"Executing query: {query} with parameter: {product_name}")  # Log the query
    #     cur.execute(query, (product_name,))
    #     rows = cur.fetchall()
    #     con.close()

    #     if not rows:
    #         return f"No customers found who bought {product_name}."
    #     return f"Customers who bought {product_name}:\n" + "\n".join([row[0] for row in rows])
    def get_sale_by_id(self, sid):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE sid = ?", (sid,))
        row = cur.fetchone()
        con.close()
        if not row:
            return "No sale found."
        return f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}"

    def get_total_sales_on_date(self, date_keyword):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        if date_keyword == "today":
            date_obj = datetime.today().date()
        elif date_keyword == "yesterday":
            date_obj = (datetime.today() - timedelta(days=1)).date()
        else:
            return "Invalid date keyword."

        cur.execute("SELECT SUM(total_price) FROM sales WHERE date = ?", (str(date_obj),))
        total = cur.fetchone()[0]
        con.close()

        return f"Total sales on {date_obj}: ₹{total}" if total else "No sales found."

    def get_total_sales_between_dates(self, start_date, end_date):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        cur.execute("SELECT SUM(total_price) FROM sales WHERE date BETWEEN ? AND ?", (start_date, end_date))
        total = cur.fetchone()[0]
        con.close()

        return f"Total sales from {start_date} to {end_date}: ₹{total}" if total else "No sales found."

    def get_sale_by_name(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE LOWER(customer_name) = ?", (name.lower(),))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sale found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    def get_sale_by_product(self, name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE LOWER(product_name) = ?", (name.lower(),))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sale found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    def get_sale_by_category(self, category):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT name FROM product WHERE category LIKE ?", ('%' + category + '%',))
        products = cur.fetchall()
        if not products:
            con.close()
            return "No products found in this category."
        product_names = [product[0] for product in products]
        placeholders = ','.join(['?'] * len(product_names))
        cur.execute(f"SELECT * FROM sales WHERE product_name IN ({placeholders})", product_names)
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sales found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    def get_sale_by_qty(self, condition, value):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        query = f"SELECT * FROM sales WHERE CAST(quantity AS INTEGER) {condition} ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sale found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    def get_sale_by_price(self, condition, value):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        query = f"SELECT * FROM sales WHERE CAST(price AS REAL) {condition} ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sale found."
        return "\n".join([f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}" for row in rows])

    def get_most_sold_product(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT product_name, SUM(quantity) as total_qty FROM sales GROUP BY product_name ORDER BY total_qty DESC LIMIT 1")
        row = cur.fetchone()
        con.close()
        return f"Most sold product: {row[0]} (Quantity: {row[1]})" if row else "No sales found."

    def get_revenue_by_category(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("""
            SELECT p.category, SUM(s.total_price)
            FROM sales s
            JOIN product p ON s.product_name = p.name
            GROUP BY p.category
        """)
        rows = cur.fetchall()
        con.close()
        if not rows:
            return "No sales data found."
        return "\n".join([f"{row[0]}: ₹{row[1]}" for row in rows])

    def get_products_sold_more_than(self, count):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT product_name, SUM(quantity) as total_qty FROM sales GROUP BY product_name HAVING total_qty > ?", (count,))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return f"No products sold more than {count} times."
        return "\n".join([f"{row[0]}: {row[1]} units sold" for row in rows])

    def get_sales_by_category_and_date(self, category, condition_raw, date_str):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        try:
            today = datetime.today()
            if "today" in date_str.lower():
                date_obj = today.date()
            elif "yesterday" in date_str.lower():
                date_obj = (today - timedelta(days=1)).date()
            else:
                date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d').date()

            condition = "=" if condition_raw not in [">", "<", ">=", "<=", "="] else condition_raw
            query = f"""
                SELECT s.sid, s.customer_name, s.product_name, s.quantity, s.price, s.total_price, s.date
                FROM sales s
                JOIN product p ON s.product_name = p.name
                WHERE p.Category = ? AND s.date {condition} ?
            """
            cur.execute(query, (category, str(date_obj)))
            rows = cur.fetchall()
            con.close()
            if not rows:
                return "No sales found."
            return "\n".join([
                f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}"
                for row in rows
            ])
        except ValueError:
            con.close()
            return "Invalid date format. Use YYYY-MM-DD or 'today'/'yesterday'."

    def get_customers_by_product(self, product_name):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        cur.execute("SELECT DISTINCT customer_name FROM sales WHERE product_name = ?", (product_name,))
        rows = cur.fetchall()
        con.close()
        if not rows:
            return f"No customers found who bought {product_name}."
        return f"Customers who bought {product_name}:\n" + "\n".join([row[0] for row in rows])

    def get_sale_by_date(self, condition_raw, date_str):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        today = datetime.today()
        yesterday = today - timedelta(days=1)

        try:
            # Normalize keywords
            if "today" in date_str.lower():
                date_obj = today.date()
            elif "yesterday" in date_str.lower():
                date_obj = yesterday.date()
            else:
                # Try to parse date in format YYYY-MM-DD
                date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d').date()

            # Map human-readable conditions
            condition_map = {
                "before": "<",
                "after": ">",
                "on": "=",
                "<": "<",
                ">": ">",
                "<=": "<=",
                ">=": ">=",
                "=": "="
            }

            condition = condition_map.get(condition_raw, "=")

            query = f"SELECT * FROM sales WHERE DATE(date) {condition} DATE(?)"
            cur.execute(query, (str(date_obj),))
            rows = cur.fetchall()
            con.close()

            if not rows:
                return "No sales found on that date."
            return "\n".join([
                f"ID: {row[0]}, customer: {row[1]}, product: {row[2]}, qty: {row[3]}, Price: {row[4]}, total price: {row[5]}, Date: {row[6]}"
                for row in rows
            ])
        except ValueError:
            con.close()
            return "Invalid date format. Use YYYY-MM-DD or 'today'/'yesterday'."

            if "total sales today" in user_input_lower:
                return self.get_total_sales_on_date("today")



        except Exception as e:
            return f"Date parsing error: {e}"
    # ========== ChatterBot Response Handler ==========    
    def handle_user_input(self, user_input):
        user_input_lower = user_input.lower()

        if "exit" in user_input_lower:
            return "exit"
        
         # === search conditions for employee ===
        if any(kw in user_input_lower for kw in ["all employees", "employee list", "employees list", "show employees"]):
            return self.get_all_employees()

        if "employee with id" in user_input_lower:
            try:
                eid = int(user_input_lower.split("id")[-1].strip(" ?"))
                return self.get_employee_by_id(eid)
            except:
                return "Invalid employee ID."

        if "employee named" in user_input_lower:
            name = user_input_lower.split("employee named")[-1].strip(" ?")
            return self.get_employee_by_name(name)

        if "employee with email" in user_input_lower:
            email = user_input_lower.split("email")[-1].strip(" ?")
            return self.get_employee_by_email(email)

        if "employee with contact" in user_input_lower:
            contact = user_input_lower.split("contact")[-1].strip(" ?")
            return self.get_employee_by_contact(contact)

        if "employee with gender" in user_input_lower:
            gender = user_input_lower.split("gender")[-1].strip(" ?")
            return self.get_employee_by_gender(gender)

        if "employee with salary" in user_input_lower:
            match = re.search(r"salary\s*(<=|>=|<|>|=|==)\s*(\d+\.?\d*)", user_input_lower)
            if match:
                condition, value = match.groups()
                return self.get_employee_by_salary(condition, value)
            else:
                return "Please use a valid comparison for salary (e.g., >= 50000)."

        if "employee with dob" in user_input_lower:
            dob = user_input_lower.split("dob")[-1].strip(" ?")
            return self.get_employee_by_dob(dob)

        if "employee with doj" in user_input_lower:
            doj = user_input_lower.split("doj")[-1].strip(" ?")
            return self.get_employee_by_doj(doj)
         # === category search conditions ===
         
        if any(kw in user_input_lower for kw in ["all categories", "category list", "categories list", "show categories"]):
            return self.get_all_category()

        if "category with id" in user_input_lower:
            try:
                cid = int(user_input_lower.split("id")[-1].strip(" ?"))
                return self.get_category_by_id(cid)
            except:
                return "Invalid category ID."

        if "category named" in user_input_lower:
            name = user_input_lower.split("category named")[-1].strip(" ?")
            return self.get_category_by_name(name)

        # === Supplier search conditions ===
        if any(kw in user_input_lower for kw in ["all suppliers", "supplier list", "suppliers list", "show suppliers"]):
            return self.get_all_suppliers()

        if "supplier named" in user_input_lower:
            name = user_input_lower.split("supplier named")[-1].strip(" ?")
            return self.get_supplier_by_name(name)

        if "supplier" in user_input_lower and "name" in user_input_lower:
            name = user_input_lower.split("name")[-1].strip(" ?")
            return self.get_supplier_by_name(name)

        if "supplier" in user_input_lower and "contact" in user_input_lower:
            contact = user_input_lower.split("contact")[-1].strip(" ?")
            return self.get_supplier_by_contact(contact)

        if "supplier" in user_input_lower and "description" in user_input_lower:
            desc = user_input_lower.split("description")[-1].strip(" ?")
            return self.get_supplier_by_description(desc)

        if "supplier" in user_input_lower and "invoice" in user_input_lower:
            try:
                invoice = int(user_input_lower.split("invoice")[-1].strip(" ?"))
                return self.get_supplier_by_invoice(invoice)
            except ValueError:
                return "Invalid invoice number."
        # === Sales Search conditions
        user_input_lower = user_input.lower()

        if any(kw in user_input_lower for kw in ["all sales", "sale list", "sales list", "show sales"]):
            return self.get_all_sales()

        if "sale with id" in user_input_lower:
            try:
                sid = int(user_input_lower.split("id")[-1].strip(" ?"))
                return self.get_sale_by_id(sid)
            except:
                return "Invalid sale ID."
        match = re.search(r"customers who bought (.+)", user_input_lower)
        if match:
            return self.get_customers_by_product(match.group(1).title())

        if "sale customer named" in user_input_lower:
            name = user_input_lower.split("sale customer named")[-1].strip(" ?")
            return self.get_sale_by_name(name)
        
        if "products sold more than" in user_input_lower:
            try:
                count = int(user_input_lower.split("products sold more than")[-1].strip(" ?"))
                return self.get_products_sold_more_than(count)
            except ValueError:
                return "Please provide a valid number after 'products sold more than'."


        if "sale of category" in user_input_lower:
            category = user_input_lower.split("sale of category")[-1].strip(" ?")
            return self.get_sale_by_category(category)
        
        if "total revenue by category" in user_input_lower:
            return self.get_revenue_by_category()
        match = re.search(r"sales of (\w+) (on|after|before)\s*(today|yesterday|\d{4}-\d{2}-\d{2})", user_input_lower)
        if match:
            category = match.group(1).title()  # Capitalize the category name
            condition = match.group(2)         # 'on', 'after', or 'before'
            date_str = match.group(3)          # 'today', 'yesterday', or specific date

            return self.get_sales_by_category_and_date(category, condition, date_str)

        if "sale of " in user_input_lower:
            category = user_input_lower.split("sale of ")[-1].strip(" ?")
            return self.get_sale_by_product(category)
        match = re.search(r"total sales between (\d{4}-\d{2}-\d{2}) and (\d{4}-\d{2}-\d{2})", user_input_lower)
        if match:
            return self.get_total_sales_between_dates(match.group(1), match.group(2))
        if "most sold product" in user_input_lower:
            return self.get_most_sold_product()

        if "sale with qty" in user_input_lower:
            match = re.search(r"qty\s*(<=|>=|<|>|=|==)\s*(\d+)", user_input_lower)
            if match:
                condition, value = match.groups()
                return self.get_sale_by_qty(condition, value)
            else:
                return "Please use a valid comparison for qty (e.g., > 10)."

        if "sale with price" in user_input_lower:
            match = re.search(r"price\s*(<=|>=|<|>|=|==)\s*(\d+\.?\d*)", user_input_lower)
            if match:
                condition, value = match.groups()
                return self.get_sale_by_price(condition, value)
            else:
                return "Please use a valid comparison for price (e.g., <= 100.50)."

        if "today's sales" in user_input_lower or "sales today" in user_input_lower or "today sale" in user_input_lower:
            today_str = datetime.today().strftime("%Y-%m-%d")
            return self.get_sale_by_date("on", today_str)

        if any(kw in user_input_lower for kw in ["sale on", "sale after", "sale before", "sale <", "sale >", "sale <=", "sale >="]):
            try:
                match = re.search(r"sale\s*(on|after|before|<=|>=|<|>)\s+(.+)", user_input_lower)
                if match:
                    condition_raw, date_str = match.groups()
                    return self.get_sale_by_date(condition_raw.strip(), date_str.strip())
            except:
                return "Invalid date condition. Try formats like 'sale after today' or 'sale < 2023/01/01'."

        # Fallback

        # === Product search conditions ===
        if any(kw in user_input_lower for kw in ["all products", "product list", "products list", "show products"]):
            return self.get_all_products()

        if "product with id" in user_input_lower:
            try:
                pid = int(user_input_lower.split("id")[-1].strip(" ?"))
                return self.get_product_by_id(pid)
            except:
                return "Invalid product ID."

        if "product named" in user_input_lower:
            name = user_input_lower.split("product named")[-1].strip(" ?")
            return self.get_product_by_name(name)

        if "product with category" in user_input_lower:
            category = user_input_lower.split("category")[-1].strip(" ?")
            return self.get_product_by_category(category)

        if "product with supplier" in user_input_lower:
            supplier = user_input_lower.split("supplier")[-1].strip(" ?")
            return self.get_product_by_supplier(supplier)

        if "product with status" in user_input_lower:
            status = user_input_lower.split("status")[-1].strip(" ?")
            return self.get_product_by_status(status)

        if "product with qty" in user_input_lower:
            match = re.search(r"qty\s*(<=|>=|<|>|=|==)\s*(\d+)", user_input_lower)
            if match:
                condition, value = match.groups()
                return self.get_product_by_qty(condition, value)
            else:
                return "Please use a valid comparison for qty (e.g., > 10)."

        if "product with price" in user_input_lower:
            match = re.search(r"price\s*(<=|>=|<|>|=|==)\s*(\d+\.?\d*)", user_input_lower)
            if match:
                condition, value = match.groups()
                return self.get_product_by_price(condition, value)
            else:
                return "Please use a valid comparison for price (e.g., <= 100.50)."

        # Fallback to ChatterBot response
        return self.chatbot.get_response(user_input)

import tkinter as tk

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#434E5A")  # Dark mode
        try:
            from tkinter import PhotoImage
            icon = PhotoImage(file="images/chatbot.png")
            self.root.iconphoto(False, icon)
        except Exception as e:
            print(f"Failed to set icon: {e}")
        self.bot = SupplierBot()  # Keep your original bot

        # Scrollable chat frame
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.place(x=10, y=10, width=470, height=450)
        self.scrollbar.place(x=480, y=10, height=450)

        self.chat_frame = self.scrollable_frame

        # Input field
        self.user_input = tk.Entry(self.root, width=60, bg="#2d2d2d", fg="white", insertbackground="white")
        self.user_input.place(x=10, y=470, width=380, height=30)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        # self.send_button = tk.Button(self.root, text="Send", width=10, command=self.send_message,
        #                              bg="#0078D7", fg="white", activebackground="#005a9e")
        # self.send_button.place(x=400, y=470, width=80, height=30)
        from tkinter import PhotoImage

# Load the image (must be done before button creation)
        self.send_icon = PhotoImage(file="images/side.png")  # Keep a reference!

        # Replace text with image
        self.send_button = tk.Button(self.root, image=self.send_icon, command=self.send_message,
                                    bg="#0078D7", activebackground="#005a9e", borderwidth=0)
        self.send_button.place(x=400, y=470, width=80, height=30)


    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You: " + user_message, "right")
            bot_response = self.bot.handle_user_input(user_message)
            self.display_message("Bot: " + str(bot_response), "left")
            self.user_input.delete(0, tk.END)

    def display_message(self, message, side):
        # Align message left/right
        message_box = tk.Label(
            self.chat_frame,
            text=message,
            anchor="e" if side == "right" else "w",
            justify="left",
            wraplength=400,
            bg="#2a2a2a" if side == "right" else "#444444",
            fg="white",
            font=('Helvetica', 10),
            padx=10,
            pady=5
        )
        message_box.pack(anchor="e" if side == "right" else "w", padx=10, pady=5, fill="x")

        self.chat_frame.update_idletasks()
        self.canvas.yview_moveto(1.0)  # Auto scroll

if __name__ == "__main__":
    root = tk.Tk()
    chat_gui = ChatGUI(root)
    root.mainloop()
