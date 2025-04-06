
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from new import SaleDashboard
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from customtkinter import *
# from GenerateBill import BillingSystem
import json
from billing import billClass
from sales_prediction import SalesTrend
from chatbot import StockChatbot
import sqlite3

def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,gender TEXT,contact TEXT,dob TEXT,doj TEXT,pass TEXT,utype TEXT,address TEXT,salary TEXT)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,contact TEXT,desc TEXT)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category TEXT, Supplier TEXT,name TEXT,price TEXT,qty TEXT,status TEXT)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS sales (sid INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, product_name TEXT, quantity INTEGER, price REAL, total_price REAL, date TEXT)")
    con.commit()
    con.close()

create_db()

theme_file = "midnight.json"

if os.path.exists(theme_file):
    with open(theme_file, "r") as file:
        theme_data = json.load(file)
else:
    print("Theme file not found! Using default theme.")
    theme_data = {}

# Set Appearance Mode (Dark)
set_appearance_mode(theme_data.get("mode", "Light"))

class IMS(CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Stock Management System")
        self.geometry("1200x700+100+50")

        # Load Colors from Theme
        bg_color = theme_data.get("background", {}).get("color", "#263238")
        frame = theme_data['CTkFrame']
        button = theme_data['CTkButton']
        sidebar=theme_data['CTkOptionMenu']
        lable=theme_data['CTkLabel']
        sidebar_color = theme_data.get("sidebar", {}).get("color", "#1E272C")
        sidebar_text = theme_data.get("sidebar", {}).get("text_color", "#90A4AE")
        titlebar_color = theme_data.get("titlebar", {}).get("color", "#37474F")
        title_text = theme_data.get("titlebar", {}).get("text_color", "#FFFFFF")
        label_color = theme_data.get("label", {}).get("text_color", "#FFFFFF")
        button_fg = theme_data.get("button", {}).get("fg_color", "#37474F")
        button_hover = theme_data.get("button", {}).get("hover_color", "#455A64")
        button_text = theme_data.get("button", {}).get("text_color", "#FFFFFF")

        # Set Background Color
        self.configure(bg=bg_color)

        # Load Images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "images", "logo.png")
        

        self.icon_title = CTkImage(light_image=Image.open(logo_path), size=(50, 50))
        employee_icon = CTkImage(light_image=Image.open("images/emp.png"), size=(50, 50))
        supplier_icon = CTkImage(light_image=Image.open("images/sup.png"), size=(50, 50))
        category_icon = CTkImage(light_image=Image.open("images/cat.png"), size=(50, 50))
        product_icon = CTkImage(light_image=Image.open("images/pro.png"), size=(50, 50))
        sales_icon = CTkImage(light_image=Image.open("images/sales.png"), size=(50, 50))
        
        employee_icon_btn = CTkImage(Image.open("images/emp.png"), size=(20, 20))
        supplier_icon_btn = CTkImage(Image.open("images/sup.png"), size=(20, 20))
        category_icon_btn = CTkImage(Image.open("images/cat.png"), size=(20, 20))
        product_icon_btn = CTkImage(Image.open("images/pro.png"), size=(20, 20))
        sales_icon_btn = CTkImage(Image.open("images/sales.png"), size=(20, 20))
        bill_icon_btn = CTkImage(Image.open("images/bill.png"), size=(20, 20))
        chatbot_icon_btn = CTkImage(Image.open("images/chatbot.png"), size=(20, 20))
        report_icon_btn = CTkImage(Image.open("images/report.png"), size=(20, 20))
                # Title Bar
        title = CTkLabel(self, text="  Stock Management System", image=self.icon_title, compound=LEFT,
                         font=("Poppins", 30, "bold"), fg_color=lable['fg_color'], text_color=lable['text_color'][0], anchor="w", padx=20)
        title.pack(fill=X, pady=5)

        # Sidebar (Left Menu)
        self.menu_frame = CTkFrame(self, width=200, corner_radius=frame["corner_radius"],
            border_width=0,
            fg_color=frame["fg_color"][0],
            border_color=frame["border_color"][0])
        self.menu_frame.pack(side=LEFT, fill=Y)
        

        lbl_menu = CTkLabel(self.menu_frame, text="Menu", font=("Poppins", 18, "bold"), text_color=lable['text_color'][0])
        lbl_menu.pack(pady=10)

        menu_buttons = [
    ("Employee", self.employee, employee_icon_btn),
    ("Supplier", self.supplier, supplier_icon_btn),
    ("Category", self.category, category_icon_btn),
    ("Products", self.product, product_icon_btn),
    ("Sales", self.sales, sales_icon_btn),
    ("Bill", self.bill, bill_icon_btn),
    ("Chatbot", self.chat, chatbot_icon_btn),
    ("Report", self.report, report_icon_btn)
]

        # Create buttons with icons
        self.menu_btns = []
        for text, command, icon in menu_buttons:
            btn = CTkButton(
                self.menu_frame, 
                text=text, 
                command=command, 
                fg_color=button['fg_color'][0], 
                hover_color=button_hover,
                text_color=button_text, 
                font=("Poppins", 14, "bold"), 
                corner_radius=10, 
                height=40, 
                width=180,
                image=icon,  
                compound="left"  
            )
            btn.pack(pady=5, padx=3)
            self.menu_btns.append(btn)

        btn_exit = CTkButton(self.menu_frame, text="Exit", command=self.quit, fg_color="red", hover_color="darkred",
                             font=("Poppins", 14, "bold"), corner_radius=10, height=40, width=180)
        btn_exit.pack(pady=10)

        # Dashboard Content
        # self.content_frame = CTkFrame(self, fg_color=bg_color)
        # self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.content_frame = CTkFrame(self, corner_radius=frame["corner_radius"],
            border_width=3,
            fg_color=frame["fg_color"][0],
            border_color=frame["border_color"][0])  # Apply light theme
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        stats = [
             ("Total Employees", "0", employee_icon),
            ("Total Suppliers", "0", supplier_icon),
            ("Total Categories", "0", category_icon),
            ("Total Products", "0", product_icon),
            ("Total Sales", "0", sales_icon)
        ]

        self.stat_labels = []
        for i, (title, value, icon) in enumerate(stats):  # Unpack all three values correctly
            lbl = CTkLabel(
                self.content_frame,
                text=f"{title}\n{value}",
                font=("Poppins", 18, "bold"),
                fg_color=button['fg_color'],
                text_color=button['text_color'][0],
                corner_radius=50,
                height=150,
                width=250,
                image=icon,  # Assign the correct image
                compound="top"  # Place image above text
            )
            lbl.grid(row=i // 3, column=i % 3, padx=50, pady=30)
            self.stat_labels.append(lbl)


        # Footer
        screen_width = self.winfo_screenwidth()
        lbl_footer = CTkLabel(self, text="Developed by Mruga Gajjar", font=("Poppins", 12),
                              fg_color=lable['fg_color'], text_color=lable['text_color'][0], width=screen_width, height=30)
        lbl_footer.place(x=0, rely=1.0, anchor="sw")

        self.update_content()

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            self.stat_labels[3].configure(text=f"Total Products\n{len(cur.fetchall())}")

            cur.execute("SELECT * FROM category")
            self.stat_labels[2].configure(text=f"Total Categories\n{len(cur.fetchall())}")

            cur.execute("SELECT * FROM employee")
            self.stat_labels[0].configure(text=f"Total Employees\n{len(cur.fetchall())}")

            cur.execute("SELECT * FROM supplier")
            self.stat_labels[1].configure(text=f"Total Suppliers\n{len(cur.fetchall())}")

            sales_count = len(os.listdir('bill')) if os.path.exists('bill') else 0
            self.stat_labels[4].configure(text=f"Total Sales\n{sales_count}")

            self.after(2000, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}")

    # Menu Actions
    def employee(self):
        self.new_win = Toplevel(self)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self)
        self.new_obj = salesClass(self.new_win)

    def bill(self):
        self.new_win = Toplevel(self)
        self.new_obj = billClass(self.new_win)

    def forecast(self):
        self.new_win = Toplevel(self)
        self.new_obj = SalesTrend(self.new_win)

    def chat(self):
        self.new_win = Toplevel(self)
        self.new_obj = StockChatbot(self.new_win)

    def report(self):
        self.new_win = Toplevel(self)
        self.new_obj = SaleDashboard(self.new_win)

if __name__ == "__main__":
    app = IMS()
    app.mainloop()