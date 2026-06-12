from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
from PIL import Image, ImageTk
class LoginPage:
    def __init__(self,master):
        self.master=master
        self.master.title("Login System")
        self.master.geometry("1350x700+0+0")
        self.master.config(bg="#fafafa")
  

        self.conn = sqlite3.connect('employee_data.db')
        self.cursor = self.conn.cursor()    
        
        #====== title==========
        title=Label(self.master,text="Inventory Management system",font=("goudy old style",40,"bold"),bg='#0f4d7d',fg="white").place(x=0,y=0,relwidth=1,height=70)
       
        
        
        #===Login Frame===========
        self.User_id=StringVar()
        self.password=StringVar()
     
        login_Frame=Frame(self.master,bd=2,relief=RIDGE,bg="#ECECEC")
        login_Frame.place(x=450,y=120,width=460,height=470)
      
        User_id=StringVar()
      
        self.User_id_label = tk.Label(login_Frame, text="User ID:",font=("Arial Rounded MT Bold",20),fg="#767171")
        self.User_id_label.place(x=80,y=70)
        self.User_id_entry = tk.Entry(login_Frame,font=("times new roman",17))
        self.User_id_entry.place(x=80,y=130,width=250)

        self.password_label = tk.Label(login_Frame, text="Password:",font=("Arial Rounded MT Bold",20),fg="#767171")
        self.password_label.place(x=80,y=180)
        self.password_entry = tk.Entry(login_Frame, show="*",font=("times new roman",15))
        self.password_entry.place(x=80,y=230,width=250)

        self.login_button = tk.Button(login_Frame, text="Login", command=self.login,font=("Arial Rounded MT Bold",18),bg="#00B0F0",activebackground="#00B0F0",fg="white",bd=2,activeforeground="white",cursor="hand2")
        self.login_button.place(x=100,y=300,width=150,height=35)

        self.register_button = tk.Button(login_Frame,cursor="hand2",text="Register New Account?",command=self.open_register,font=("times new roman",15),bd=0,fg="black")
        self.register_button.place(x=80,y=350)
   
     
    def login(self):
        User_id = self.User_id_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT access_level FROM employees WHERE User_id=? AND password=?", (User_id, password))
        result = self.cursor.fetchone()

        if result:
            access_level = result[0]
            if access_level == 'admin':
                self.open_dashboard()
            elif access_level == 'employee':
                self.open_bill()
            else:
                messagebox.showerror("Error", "Invalid access level.")
        else:
            messagebox.showerror("Error", "Invalid Employee ID or Password.")

    def open_dashboard(self):
        self.master.withdraw()
        try:
            subprocess.Popen([sys.executable, "s.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "s.py not found.")
        self.master.deiconify()

    def open_bill(self):
        self.master.withdraw()
        try:
            subprocess.Popen([sys.executable, "billing.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "billing.py not found.")
        self.master.deiconify()

    def open_register(self):
        try:
            subprocess.Popen([sys.executable, "register.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "register.py not found.")

         
                     
   
    def open_register(self):
        try:
            subprocess.Popen([sys.executable, "register.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "register.py not found.")

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
