from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
import datetime


class billClass:
    def __init__(self,root):    
        self.root=root
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.geometry("1350x700+110+80")
        self.root.title("Stock Management System ")
        # self.root.resizable(False,False)
        self.root.config(bg="#434E5A")
        self.cart_list=[]
        self.chk_print=0

        #------------- title --------------
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Stock Management System",image=self.icon_title,compound=LEFT,font=("Poppins",40,"bold"),bg="#434E5A",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #------------ logout button -----------
        # btn_logout=Button(self.root,text="Logout",font=("Poppins",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("Poppins",15),bg="#434E5A",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #------------ footer -----------------
        lbl_footer=Label(self.root,text="Stock Management System | Developed Mruga Gajjar\nFor any Technical Issues Contact: 9899459288",font=("Poppins",10),bg="#434E5A",fg="white").pack(side=BOTTOM,fill=X)

        #-------------- product frame -----------------
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="#434E5A")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All Products",font=("Poppins",20,"bold"),bg="#BCC6D0",fg="#434E5A").pack(side=TOP,fill=X)
        
        self.var_search=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="#434E5A")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,fg='#BCC6D0',text="Search Product | By Name",font=("Poppins",15,"bold"),bg="#434E5A").place(x=2,y=5)
        
        lbl_search=Label(ProductFrame2,fg='#BCC6D0',text="Product Name",font=("Poppins",15,"bold"),bg="#434E5A").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("Poppins",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("Poppins",15),bg="#434E5A",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("Poppins",15),bg="#434E5A",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)\
        
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="P ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        lbl_note=Label(ProductFrame1,text="Note: 'Enter 0 Quantity to remove product from the Cart'",font=("Poppins",12),anchor="w",bg="#434E5A",fg="red").pack(side=BOTTOM,fill=X)

        #-------------- customer frame ---------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="#434E5A")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,fg='#434E5A',text="Customer Details",font=("Poppins",15),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,fg='#BCC6D0',text="Name",font=("Poppins",15),bg="#434E5A").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,fg='black',textvariable=self.var_cname,font=("Poppins",13),bg="lightyellow").place(x=80,y=35,width=180)
        
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("Poppins",15),bg="#434E5A",fg='#BCC6D0').place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,fg='black',textvariable=self.var_contact,font=("Poppins",15),bg="lightyellow").place(x=380,y=35,width=140)

        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="#434E5A")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #--------------- calculator frame ---------------------
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="#434E5A")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,fg='white',bg='#34495e',text=7,font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,fg='white',bg='#34495e',text=8,font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,fg='white',bg='#34495e',text=9,font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,fg='white',bg='#34495e',text="+",font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,fg='white',bg='#34495e',text=4,font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,fg='white',bg='#34495e',text=5,font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,fg='white',bg='#34495e',text=6,font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,fg='white',bg='#34495e',text="-",font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,fg='white',bg='#34495e',text=1,font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,fg='white',bg='#34495e',text=2,font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,fg='white',bg='#34495e',text=3,font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,fg='white',bg='#34495e',text="*",font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,fg='white',bg='#34495e',text=0,font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,fg='white',bg='#34495e',text="C",font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,fg='white',bg='#34495e',text="=",font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,fg='white',bg='#34495e',text="/",font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)

        #------------------ cart frame --------------------
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Products: [0]",font=("Poppins",12),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)\
        
        self.CartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=100)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=30)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #-------------- add cart widgets frame ---------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="#434E5A")
        Add_CartWidgets_Frame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgets_Frame,fg='#BCC6D0',text="Product Name",font=("Poppins",15),bg="#434E5A").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgets_Frame,fg='black',textvariable=self.var_pname,font=("Poppins",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgets_Frame,fg='#BCC6D0',text="Price Per Qty",font=("Poppins",15),bg="#434E5A").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgets_Frame,fg='black',textvariable=self.var_price,font=("Poppins",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgets_Frame,fg='#BCC6D0',text="Quantity",font=("Poppins",15),bg="#434E5A").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgets_Frame,fg='black',textvariable=self.var_qty,font=("Poppins",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_inStock=Label(Add_CartWidgets_Frame,fg='#BCC6D0',text="In Stock",font=("Poppins",15),bg="#434E5A")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgets_Frame,command=self.clear_cart,text="Clear",font=("Poppins",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgets_Frame,command=self.add_update_cart,text="Add | Update",font=("Poppins",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
        
        #------------------- billing area -------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="#434E5A")
        billFrame.place(x=953,y=110,width=400,height=410)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("Poppins",20,"bold"),bg="#BCC6D0",fg="#434E5A").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #------------------- billing buttons -----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="#434E5A")
        billMenuFrame.place(x=953,y=520,width=400,height=140)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("Poppins",15,"bold"),bg="dodger blue",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("Poppins",15,"bold"),bg="dodger blue",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("Poppins",15,"bold"),bg="dodger blue",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text="Save",command=self.print_bill,cursor="hand2",font=("Poppins",15,"bold"),bg="MediumPurple3",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("Poppins",15,"bold"),bg="red",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,cursor="hand2",font=("Poppins",15,"bold"),bg="PaleVioletRed3",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

        self.show()
        #self.bill_top()
        self.update_date_time()
#---------------------- all functions ------------------------------
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error","Please select product from the list",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #---------- update cart --------------
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present="yes"
                    break
                index_+=1
            if present=="yes":
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.siscount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
        else:
            #--------- bill top -----------------
            self.bill_top()
            #--------- bill middle --------------
            self.bill_middle()
            #--------- bill bottom --------------
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been generated",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tGucci 
\t Phone No. 9899459288 , Gujrat-380061
{str("="*46)}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #------------- update qty in product table --------------
                cur.execute("update product set qty=?,status=? where pid=?",(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print=0
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Stock Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    # def print_bill(self):
    #     if self.chk_print == 1:
    #         try:
    #             customer_name = self.var_cname.get().replace(" ", "_")  # Replace spaces with underscores
    #             file_path = f'bill/{customer_name}_{str(self.invoice)}.txt'
                
    #             with open(file_path, 'w') as file:
    #                 file.write(self.txt_bill_area.get('1.0', END))

    #             messagebox.showinfo("Saved", f"Bill has been saved as {file_path}", parent=self.root)
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Failed to save bill: {str(e)}", parent=self.root)
    #     else:
    #         messagebox.showinfo("Print", "Please generate a bill before saving.", parent=self.root)


    
    def print_bill(self):
        print("🔹 print_bill method called!")  # Debug

        if self.chk_print == 1:
            try:
                customer_name = str(self.var_cname.get()).strip().replace(" ", "_")
                if not customer_name:
                    messagebox.showerror("Error", "Customer name cannot be empty!", parent=self.root)
                    return

                file_path = f'bill/{customer_name}_{str(self.invoice)}.txt'

                with open(file_path, 'w') as file:
                    file.write(self.txt_bill_area.get('1.0', 'end'))

                con = sqlite3.connect("ims.db")
                cur = con.cursor()

                print("🛒 Cart List:", self.cart_list)  # Debug

                if not self.cart_list:
                    messagebox.showwarning("Warning", "Cart is empty! No items to save in Sales.", parent=self.root)
                    return

                for item in self.cart_list:
                    if len(item) < 5:  # Ensure all values exist
                        print("❌ Skipping item due to missing data:", item)
                        continue  

                    product_id = item[0]  # Assuming '7' is Product ID
                    product_name = item[1]  # 'Denim Joggers'
                    price = float(item[2])  # '899'
                    quantity = int(item[3])  # '2'
                    discount = float(item[4])  # '30' (Assuming it's discount % or amount)

                    total_price = (price * quantity) - discount  # Apply discount
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(f"📌 Inserting: {self.invoice}, {self.var_cname.get()}, {product_name}, {quantity}, {price}, {total_price}, {date}")

                    cur.execute("""
                        INSERT INTO sales (customer_name, product_name, quantity, price, total_price, date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (self.var_cname.get(), product_name, quantity, price, total_price, date))



                print("✅ Committing data to database...")
                con.commit()

                messagebox.showinfo("Saved", f"Bill saved as {file_path}\nDetails added to Sales!", parent=self.root)

            except sqlite3.Error as db_err:
                print(f"❌ Database Error: {db_err}")  # Debug
                messagebox.showerror("Database Error", f"Failed to save to database: {str(db_err)}", parent=self.root)
            except Exception as e:
                print(f"❌ General Error: {e}")  # Debug
                messagebox.showerror("Error", f"Failed to save bill: {str(e)}", parent=self.root)
            finally:
                con.close()
                print("🔗 Database connection closed.")

        else:
            messagebox.showinfo("Print", "Please generate a bill before saving.", parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()