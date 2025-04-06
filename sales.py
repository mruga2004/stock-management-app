from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
from customtkinter import *
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Stock Management System ")
        self.root.config(bg="#434E5A")
        self.root.resizable(False,False)
        self.root.focus_force()

        self.blll_list=[]
        self.var_invoice=StringVar()
        #--------------- title ---------------------
        lbl_title=Label(self.root,text="View Customer Bills",font=("Poppins",30),bg="#E5E9F0",fg="#434E5A",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice=Label(self.root,text="Invoice No.",font=("Poppins",15),bg="#434E5A",fg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("Poppins",15),bg="lightyellow",fg="#111").place(x=160,y=100,width=180,height=28)

        btn_search=CTkButton(self.root,text="Search",command=self.search,font=("Poppins",15,"bold"),fg_color="#2196f3",text_color="#111",cursor="hand2",width=120,height=28).place(x=360,y=100)
        btn_clear=CTkButton(self.root,text="Clear",command=self.clear,font=("Poppins",15,"bold"),fg_color="lightgray",text_color="#434E5A",cursor="hand2").place(x=490,y=100)

        #----------------- bill list -------------------
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("Poppins",15),bg="#434E5A",fg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #--------------- bill area ----------------------
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=800,height=330)
        
        lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("Poppins",20),bg="orange",fg="white").pack(side=TOP,fill=X)
        
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #------------- image -----------------
        # self.bill_photo=Image.open("images/cat2.png")
        # self.bill_photo=self.bill_photo.resize((350,200))
        # self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        # lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        # lbl_image.place(x=710,y=110)
        
        self.show()
#----------------------------------------------------------------------------------------------------
    def show(self):
        del self.blll_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.blll_list.append(i.split('.')[0])

    
    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if index_:
            file_name = self.Sales_List.get(index_)
            file_path = f'bill/{file_name}'

            if os.path.exists(file_path):  # Check if the file exists
                self.bill_area.delete('1.0', END)
                with open(file_path, 'r') as fp:
                    self.bill_area.insert(END, fp.read())  # Read the entire file at once
            else:
                messagebox.showerror("Error", "File not found!", parent=self.root)

    def search(self):
        invoice_file = f'bill/{self.var_invoice.get()}.txt'
        
        if not self.var_invoice.get():
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        elif os.path.exists(invoice_file):
            self.bill_area.delete('1.0', END)
            with open(invoice_file, 'r') as fp:
                self.bill_area.insert(END, fp.read())
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)


if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()