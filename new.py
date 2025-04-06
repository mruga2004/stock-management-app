from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

class SaleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1150x700+200+50")
        self.root.title("Report")
        self.root.config(bg="#434E5A")
        self.root.resizable(False, False)

        self.after_ids = []

        lbl_title = Label(self.root, text="Report", font=("Poppins", 30), bg="#E5E9F0", fg="#434E5A", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        self.report_frame = Frame(self.root, bg="#434E5A")
        self.report_frame.place(x=50, y=100, width=400, height=480)

        self.chart_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.chart_frame.place(x=420, y=90, width=700, height=530)

        self.safe_update_report()
        self.safe_draw_graph("month")

        Button(self.root, text="Daily", font=("Poppins", 12), bg="#2196f3", fg="white",
               command=lambda: self.safe_draw_graph("day"), cursor="hand2").place(x=470, y=630, width=100)

        Button(self.root, text="Weekly", font=("Poppins", 12), bg="#2196f3", fg="white",
               command=lambda: self.safe_draw_graph("week"), cursor="hand2").place(x=580, y=630, width=100)

        Button(self.root, text="Monthly", font=("Poppins", 12), bg="#2196f3", fg="white",
               command=lambda: self.safe_draw_graph("month"), cursor="hand2").place(x=690, y=630, width=100)

        Button(self.root, text="Yearly", font=("Poppins", 12), bg="#2196f3", fg="white",
               command=lambda: self.safe_draw_graph("year"), cursor="hand2").place(x=800, y=630, width=100)

        Button(self.root, text="Export CSV", font=("Poppins", 12), bg="#4CAF50", fg="white",
               command=self.export_data, cursor="hand2").place(x=910, y=630, width=120)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_sales_data(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT product_name, quantity, date FROM sales")
        rows = cur.fetchall()
        con.close()
        df = pd.DataFrame(rows, columns=["product", "qty", "date"])
        df["date"] = pd.to_datetime(df["date"])
        return df

    def update_report(self):
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        total = self.get_total_sales()
        top_product, top_qty = self.get_top_product()
        low_stock = self.get_low_stock()

        Label(self.report_frame, text=f"Total Sales: ₹{total:.2f}", font=("Poppins", 15), bg="#434E5A", fg="white").pack(pady=10)
        Label(self.report_frame, text=f"Top Product: {top_product} ({top_qty})", font=("Poppins", 14), bg="#434E5A", fg="white").pack(pady=10)

        Label(self.report_frame, text="Low Stock Items:", font=("Poppins", 14, "bold"), bg="#434E5A", fg="orange").pack(pady=5)
        if low_stock:
            for name, qty in low_stock:
                Label(self.report_frame, text=f"{name} ({qty})", font=("Poppins", 13), bg="#434E5A", fg="white").pack(anchor="w", padx=20)
        else:
            Label(self.report_frame, text="✔ All items in stock", font=("Poppins", 12), bg="#434E5A", fg="lightgreen").pack(pady=10)

    def safe_update_report(self):
        try:
            self.update_report()
        except Exception as e:
            print("Error in update_report:", e)

    def get_total_sales(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT SUM(total_price) FROM sales")
        total = cur.fetchone()[0] or 0
        con.close()
        return total

    def get_top_product(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT product_name, SUM(quantity) FROM sales GROUP BY product_name ORDER BY SUM(quantity) DESC LIMIT 1")
        result = cur.fetchone()
        con.close()
        return result if result else ("N/A", 0)

    def get_low_stock(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT name, qty FROM product WHERE CAST(qty AS INTEGER) <= 5")
        results = cur.fetchall()
        con.close()
        return results

    def draw_graph(self, timeframe):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        df = self.get_sales_data()
        if df.empty:
            Label(self.chart_frame, text="No sales data available", font=("Poppins", 14), bg="white", fg="red").pack()
            return

        period_map = {"year": "Y", "month": "M", "week": "W", "day": "D"}
        df["period"] = df["date"].dt.to_period(period_map.get(timeframe, "M"))
        pivot = df.groupby(["period", "product"])[["qty"]].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        products = pivot["product"].unique()
        x_vals = sorted(pivot["period"].unique())

        width = 0.8 / len(products)
        offsets = [-width * (len(products) - 1) / 2 + i * width for i in range(len(products))]

        for offset, product in zip(offsets, products):
            sub = pivot[pivot["product"] == product]
            x = [x_vals.index(p) + offset for p in sub["period"]]
            ax.bar(x, sub["qty"], width=width, label=product)
            for xi, y in zip(x, sub["qty"]):
                ax.text(xi, y, f"{int(y)}", ha='center', va='bottom', fontsize=7)

        ax.set_title(f"Product-wise Sales ({timeframe.title()})")
        ax.set_xlabel("Period")
        ax.set_ylabel("Quantity Sold")
        ax.set_xticks(range(len(x_vals)))
        ax.set_xticklabels([str(p) for p in x_vals], rotation=45, ha='right', fontsize=7)
        ax.legend()
        plt.tight_layout()
        fig.subplots_adjust(bottom=0.35)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def safe_draw_graph(self, timeframe):
        try:
            self.draw_graph(timeframe)
        except Exception as e:
            print("Error in draw_graph:", e)

    def export_data(self):
        try:
            df = self.get_sales_data()
            if df.empty:
                messagebox.showinfo("No Data", "No sales data available to export.")
                return

            export_path = "sales_report.csv"
            df.to_csv(export_path, index=False)
            messagebox.showinfo("Success", f"Sales data exported to:\n{os.path.abspath(export_path)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data:\n{str(e)}")

    def on_closing(self):
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = SaleDashboard(root)
    root.mainloop()
