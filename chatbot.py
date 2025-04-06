import sqlite3
import tkinter as tk
from tkinter import scrolledtext

class StockChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Chatbot")
        self.root.geometry("500x500")

        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # self.root.geometry(f"{screen_width}x{screen_height}+0+0")        
        self.root.configure(bg="#434E5A")
        
        # Chat Display Area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=55, height=20, state='disabled')
        self.chat_area.pack(pady=10)
        
        # Entry Field with Placeholder
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, width=40, fg='gray')
        self.entry.insert(0, "Enter product name...")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.pack(pady=5)
        
        # Button to Check Stock
        self.send_button = tk.Button(self.root, text="Check Stock", command=self.check_stock)
        self.send_button.pack()
        
        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.check_stock())
    
    def clear_placeholder(self, event):
        if self.entry_var.get() == "Enter product name...":
            self.entry_var.set("")
            self.entry.config(fg='black')
    
    def restore_placeholder(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter product name...")
            self.entry.config(fg='gray')
    
    def check_stock(self):
        product_name = self.entry_var.get().strip()
        if not product_name or product_name == "Enter product name...":
            return
        
        stock = self.get_stock_from_db(product_name)
        response = f"Stock for '{product_name}': {stock} units" if stock is not None else "Product not found."
        self.update_chat(f"You: {product_name}\nBot: {response}\n")
        
    def get_stock_from_db(self, product_name):
        try:
            con = sqlite3.connect("ims.db")
            cur = con.cursor()
            cur.execute("SELECT qty FROM product WHERE name=?", (product_name,))
            row = cur.fetchone()
            con.close()
            return row[0] if row else None
        except Exception as ex:
            return "Error fetching data."
    
    def update_chat(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message)
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = StockChatbot(root)
    root.mainloop()