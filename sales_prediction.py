from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class SalesTrend:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x650+320+120")
        self.root.title("Sales Trend Analysis")
        self.root.config(bg="#111")
        self.root.resizable(False, False)

        # Database
        self.db_name = "ims.db"

        # Variables
        self.var_product = StringVar()

        # Title
        lbl_title = Label(self.root, text="Sales Trend Analysis", font=("Poppins", 20), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=10)

        # Product Selection
        lbl_product = Label(self.root, text="Select Product:", font=("Poppins", 14), bg="#111", fg="white")
        lbl_product.place(x=50, y=80)

        self.cmb_product = ttk.Combobox(self.root, textvariable=self.var_product, font=("Poppins", 12), state="readonly")
        self.cmb_product.place(x=180, y=80, width=250, height=30)
        self.load_products()

        btn_show = Button(self.root, text="Show Trend", command=self.plot_sales_trend, font=("Poppins", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_show.place(x=450, y=80, width=120, height=30)

        # Graph Frame
        self.frame_graph = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.frame_graph.place(x=50, y=130, width=1000, height=300)

        # Table Frame
        self.frame_table = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.frame_table.place(x=50, y=450, width=1000, height=180)

        # Table
        self.create_table()

    # Load Product Names into Dropdown
    def load_products(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("SELECT DISTINCT product_name FROM sales")
        products = [row[0] for row in cur.fetchall()]
        con.close()

        if products:
            self.cmb_product["values"] = products
            self.cmb_product.current(0)  # Select first item by default
        else:
            self.cmb_product["values"] = ["No Products Found"]

    # Plot Sales Trend
    def plot_sales_trend(self):
        product = self.var_product.get()
        if not product:
            messagebox.showerror("Error", "Please select a product", parent=self.root)
            return

        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        # Fetch last 30 days of sales data
        cur.execute("""
            SELECT date(date), SUM(quantity) FROM sales
            WHERE product_name = ? 
            AND date(date) >= date('now', '-30 days')
            GROUP BY date(date)
            ORDER BY date(date)
        """, (product,))
        data = cur.fetchall()
        con.close()

        if not data:
            messagebox.showinfo("No Data", f"No sales data found for {product} in the last 30 days.", parent=self.root)
            return

        # Extract dates and sales quantities
        dates, sales = zip(*data)
        dates = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]

        # Clear previous graph
        for widget in self.frame_graph.winfo_children():
            widget.destroy()

        # Plot Graph
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(dates, sales, marker='o', linestyle='-', color='b', label="Sales Trend (Last 30 Days)")

        ax.set_title(f"Sales Trend for {product} (Last 30 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Quantity Sold")
        ax.legend()
        ax.grid()

        # Embed Graph in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Load Table Data
        self.load_sales_table(product)

    # Create Sales Data Table
    def create_table(self):
        columns = ("sid", "customer_name", "product_name", "quantity", "price", "total_price", "date")

        self.sales_table = ttk.Treeview(self.frame_table, columns=columns, show="headings")
        self.sales_table.pack(fill=BOTH, expand=True)

        for col in columns:
            self.sales_table.heading(col, text=col.replace("_", " ").title())
            self.sales_table.column(col, width=100)

    # Load Sales Data into Table
    def load_sales_table(self, product):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE product_name = ?", (product,))
        rows = cur.fetchall()
        con.close()

        self.sales_table.delete(*self.sales_table.get_children())  # Clear old data

        for row in rows:
            self.sales_table.insert("", END, values=row)  # Insert new data

if __name__ == "__main__":
    root = Tk()
    obj = SalesTrend(root)
    root.mainloop()
