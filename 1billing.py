from tkinter import*
from PIL import Image,ImageTk  #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System |Developed By Roshani")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #====== title==========
        self.icon_title=PhotoImage(file="image\window.png")
        title=Label(self.root,text="Inventory Managemnet system",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        #==btn_Logout====
       # btn_logout=Button(self.root,text="Logout",command=self.logout,font=("time new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("time new roman",15,"bold"),bg='#0f4d7d',fg="white",cursor="hand2").place(x=1100,y=10,height=50,width=150)
       
        #=====clock======
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Managemnet system\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15,"bold"),bg="#4D636D",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #=======Product Frame1================
        #self.var_search=StringVar()
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=530)
        
        ptitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
       
       #=========Product Search Frame========
       
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=95)
        
        lbl_Search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=6)
        
        lbl_Search=Label(ProductFrame2,text=" Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=49)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=133,y=51,width=150,height=25)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=287,y=49,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=287,y=14,width=100,height=28)
  
  
        #============== Product Details Frrame=================
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=355)
        
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
    
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("id", "name", "stock", "price","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("id",text="ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("stock",text="Stock")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("status",text="Status")
        
        self.product_Table["show"]="headings"
        
        self.product_Table.column("id",width=60)
        self.product_Table.column("name",width=200)
        self.product_Table.column("stock",width=70)
        self.product_Table.column("price",width=70)
        self.product_Table.column("status",width=80)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
      
       # lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",13),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
       
       
#=================Customer Frame=====================================================
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=500,height=80)
        
        ctitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=70,y=35,width=160)
        
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=245,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=345,y=35,width=145)
        
        Cal_Cart_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=500,height=330)#height=350
    
       
        #==================Calculator cart frame ==============
        self.var_cal_input=StringVar()
        
        Cal_Frame=Frame(Cal_Cart_Frame,bd=7,relief=RIDGE,bg="white")
        Cal_Frame.place(x=3,y=25,width=260,height=287)#width=251#height=320
        
        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',26,"bold"),width=12,bd=9,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7=Button(Cal_Frame,text=7,font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=7,width=3,padx=2,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text=8,font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=7,width=3,padx=2,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text=9,font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=7,width=3,padx=2,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=7,width=3,padx=2,cursor="hand2").grid(row=1,column=3)
       
        
        btn_4=Button(Cal_Frame,text=4,font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=7,width=3,padx=2,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text=5,font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=7,width=3,padx=2,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text=6,font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=7,width=3,padx=2,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=7,width=3,padx=2,cursor="hand2").grid(row=2,column=3)
       
        btn_1=Button(Cal_Frame,text=1,font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=7,width=3,padx=2,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text=2,font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=7,width=3,padx=2,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text=3,font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=7,width=3,padx=2,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=7,width=3,padx=2,cursor="hand2").grid(row=3,column=3)
       
        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=7,width=3,padx=2,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=7,width=3,padx=2,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=7,width=3,padx=2,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=7,width=3,padx=2,cursor="hand2").grid(row=4,column=3)
       
   
        
       #================== cart Frame==============
        
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=265,y=24,width=227,height=288)
       
       
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Product:[0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
      
        
        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)
       
        self.CartTable=ttk.Treeview(Cart_Frame,columns=("id","name","stock","price"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("id",text="ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("stock",text="Stock")
        self.CartTable.heading("price",text="Price")
       
        
        self.CartTable["show"]="headings"
        
        self.CartTable.column("id",width=60)
        self.CartTable.column("name",width=150)
        self.CartTable.column("stock",width=90)
        self.CartTable.column("price",width=40)
      
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
       
       
       #==================ADD cart Button==============
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=530,width=500,height=110)
        
        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=4,y=4)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=30,width=190,height=25)
        
        
        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=220,y=4)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=220,y=30,width=160,height=25)
        
         
        lbl_p_price=Label(Add_CartWidgetsFrame,text="Quntity",font=("times new roman",15),bg="white").place(x=400,y=4)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=30,width=95,height=25)
        
        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=3,y=65)
       
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=65,width=110,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=320,y=65,width=170,height=30)


#=============================billing area=================
        billFrame=Frame(self.root,bd=2,relief=RAISED,bg='white')
        billFrame.place(x=924,y=110,width=352,height=385)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#F44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

#======================= billing button================
        billMenuFrame=Frame(self.root,bd=2,relief=RAISED,bg='white')
        billMenuFrame.place(x=924,y=494,width=352,height=145)
        
        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=110,height=65)
    
        self.lbl_discount=Label(billMenuFrame,text='Discount \n[5%]',font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=115,y=5,width=108,height=65)
    
        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay \n[0]',font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=230,y=5,width=115,height=65)
       
       
       
        btn_print=Button(billMenuFrame,text='Print',cursor='hand2',command=self.print_bill,font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=76,width=80,height=60)
    
        btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor='hand2',font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=85,y=76,width=88,height=60)
    
        btn_generate=Button(billMenuFrame,text='Generate/Save Bill',command=self.generate_bill,cursor='hand2',font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=175,y=76,width=170,height=60)
                                                              
        self.show()
      #  self.bill_top()
        self.update_date_time()
    
    #============================== All Function=================
    
    
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)     
        
    def clear_cal(self):
        self.var_cal_input.set('')  
        
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))



    def show(self):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
          
           cur.execute("Select id,name,stock,price,status from products where status='Active'")
           rows=cur.fetchall()
           self.product_Table.delete(*self.product_Table.get_children())
           for row in rows:
               self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
    

    def search(self):  
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":  
                messagebox.showerror("Error","Search input should be required",parent=self.root)  
            else:
                cur.execute("Select id,name,stock,price,status from products where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO record found!!!",parent=self.root)  
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
        
     
    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In stock [{str(row[3])}]")
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
        self.lbl_instock.config(text=f"In stock [{str(row[4])}]")
        self.var_stock.set(row[5])
     
    def add_update_cart(self):
        if   self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select products from thr list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invaild Quantity",parent=self.root)
       
        else: 
           #price_cal=int(self.var_qty.get())*float(self.var_price.get())
           #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[ self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            
             # print(self.cart_list)
             #============update_cart========
            present='no'
            index_=0
            for row in self.cart_list:
                if  self.var_pid.get()==row[0]:
                   present='yes'
                   break
                index_+=1
            if present=='yes': 
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to update|Remove from the Cart List",parent=self.root)       
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:  
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #qty
            else:
                self.cart_list.append(cart_data)   
           
            self.show_cart() 
            self.bill_updates()
            
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))       
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}') 
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}') 
        self.cartTitle.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")   
  
    def show_cart(self):  
       
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
        
     
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
        else:
            #=====Bill Top=========
            self.bill_top()
            #=====Bill Middle======
            self.bill_middle()
            #=====Bill Bottom======
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print=1
            
            
    def bill_top(self):  
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))  
        bill_top_temp=f'''
\t\tXYZ_Inventory
\tPhone No.98765*****,Nandurbar-125001
{str("="*40)}       
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}       
{str("="*40)}
 Product Name\t\tQTY\tPrice
{str("="*40)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*40)}
 Bill Amount\t\t\tRs.{self.bill_amnt}
 Discount\t\t\tRs.{self.discount}
 Net Pay\t\t\tRs.{self.net_pay}
{str("="*40)}\n        
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
        
    def bill_middle(self): 
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:   
            for row in self.cart_list:  
                id=row[0]
                name=row[1]
                stock=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'  
                     
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t"+row[3]+"\tRs."+price) 
                #===========update stock in product table===========
                cur.execute('Update products set stock=?,status=? where id=?',(
                    stock,  
                    status,
                    id       
                ))
                con.commit()
            con.close()
            self.show()    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
            
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_stock.set('')
        self.var_qty.set('')  
        self.lbl_instock.config(text=f"In stock")
        self.var_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product:[0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0 
         
    def update_date_time(self):
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")  
            self.lbl_clock.config(text=f"Welcome to Inventory Managemnet system\t\t Date: {str(date_)}\t\t Time:{str(time_)}")
            self.lbl_clock.after(200,self.update_date_time)       

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill,to print the receipt",parent=self.root)
          

    def logout(self):
        self.root.destroy
        os.system("python login.py")




if __name__=="__main__":
   root=Tk()
   obj=BillClass(root)
   root.mainloop()     