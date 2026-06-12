# register.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
from PIL import Image, ImageTk
from tkinter import*
from tkinter import ttk,messagebox
from PIL import Image,ImageTk 
#import pymysql# pip install pymysql

import sqlite3
import os
class RegistrationPage:
    def __init__(self, master):
        self.master = master
        master.title("Regiseration Window")
        self.master.geometry("1350x700+0+0")
       # self.master.config(bg="white")
        
        self.conn = sqlite3.connect('employee_data.db')
        self.cursor = self.conn.cursor()
       
        # Load background image
        try:#ImageTk.PhotoImage#Image.open(login_background.png
            self.bg_image = Image.open("image/b2.png")  # Replace with your image path
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(master, image=self.bg_photo)
            self.bg_label.place(x=250,y=0,relwidth=1,relheight=1)#(relwidth=1, relheight=1)
    
        except FileNotFoundError:
            messagebox.showerror("Error", "login_background.png not found.")
            return
           #==========================LEFT Image=============
           # Load background image
        try:#ImageTk.PhotoImage#Image.open(login_background.png
            self.bg_image = Image.open("image/b2.png")  # Replace with your image path
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(master, image=self.bg_photo)
            self.bg_label.place(x=250,y=0,relwidth=1,relheight=1)#(relwidth=1, relheight=1)
    
        except FileNotFoundError:
            messagebox.showerror("Error", "login_background.png not found.")
            return
          
        
    #    #=========LEFT Image============
    
        try:#ImageTk.PhotoImage#Image.open(login_background.png
            self.bgg_image = Image.open("image/side.png")  # Replace with your image path
            self.bgg_photo = ImageTk.PhotoImage(self.bgg_image)
            self.bgg_label = tk.Label(master, image=self.bgg_photo)
            self.bgg_label.place(x=80,y=100,width=400,height=500)#place(x=250,y=0,relwidth=1,relheight=1)#(relwidth=1, relheight=1)
    
        except FileNotFoundError:
            messagebox.showerror("Error", "login_background.png not found.")
            return
        
        self.login_button = tk.Button(master, text="sign In",font=("times new roman",20),bd=0,cursor="hand2" ,command=self.login_window)
        self.login_button.place(x=190,y=460,width=180)#grid(row=7, column=0, columnspan=2, pady=20)

        
       
        # Create a frame for the registration elements
        self.register_frame = tk.Frame(master, bg="white",bd=2,relief="groove")
        self.register_frame.place(x=480,y=100,width=700,height=500)#place(relx=0.5, rely=0.5, anchor="center")
        
        title=Label(self.register_frame,text="REGISTER HERE",font=("time new roman",35,"bold"),bg="white",fg="green").place(x=160,y=20)
         #==================Row1================

        self.User_id_label = tk.Label(self.register_frame, text="User ID:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.User_id_label.place(x=50,y=100)#grid(row=0, column=0, padx=90, pady=90, sticky="w")
        self.User_id_entry = tk.Entry(self.register_frame,font=("time new roman",15),bg="lightgray")
        self.User_id_entry.place(x=50,y=130,width=250)#grid(row=0, column=1, padx=90, pady=90)

        self.first_name_label = tk.Label(self.register_frame, text="First Name:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.first_name_label.place(x=370,y=100)#grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.first_name_entry = tk.Entry(self.register_frame,font=("time new roman",15),bg="lightgray")
        self.first_name_entry.place(x=370,y=130,width=250)#grid(row=1, column=1, padx=10, pady=10)

        self.last_name_label = tk.Label(self.register_frame, text="Last Name:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.last_name_label.place(x=50,y=170)#grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.last_name_entry = tk.Entry(self.register_frame,font=("time new roman",15),bg="lightgray")
        self.last_name_entry.place(x=50,y=200,width=250)#grid(row=2, column=1, padx=10, pady=10

        self.email_label = tk.Label(self.register_frame, text="Email:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.email_label.place(x=370,y=170)#grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = tk.Entry(self.register_frame,font=("time new roman",15),bg="lightgray")
        self.email_entry.place(x=370,y=200,width=250)#grid(row=3, column=1, padx=10, pady=10)
       
        self.password_label = tk.Label(self.register_frame, text="Password:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.password_label.place(x=50,y=240)#grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(self.register_frame,show="*",font=("time new roman",15),bg="lightgray")
        self.password_entry.place(x=50,y=270,width=250)#grid(row=4, column=1, padx=10, pady=10)

        self.confirm_password_label = tk.Label(self.register_frame, text="Confirm Password:",font=("time new roman",15,"bold"),bg="white",fg="black")
        self.confirm_password_label.place(x=370,y=240)#grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.confirm_password_entry = tk.Entry(self.register_frame,show="*",font=("time new roman",15),bg="lightgray")
        self.confirm_password_entry.place(x=370,y=270,width=250)#grid(row=5, column=1, padx=10, pady=10)
        
        #====================Row2=================
        self.user_type_label = tk.Label(self.register_frame, text="User Type:",background="white",fg="black",font=("time new roman",15,"bold"))
        self.user_type_label.place(x=240,y=315)#grid(row=10, column=0, padx=10, pady=10, sticky="w")
        self.user_type_choices = ["Select","admin", "employee"]
        self.user_type_var = tk.StringVar(self.register_frame)
        self.user_type_var.set(self.user_type_choices[0])  # Default to employee
        self.user_type_dropdown = tk.OptionMenu(self.register_frame, self.user_type_var, *self.user_type_choices)
        self.user_type_dropdown.place(x=200,y=350,width=200)#grid(row=10, column=1, padx=10, pady=10, sticky="ew")
       # self.user_type_var.current(0)
       
       # utype=Label(self.register_frame,text="user Type:",font=("time new roman",15),bg="white",fg="gray").place(x=240,y=315)  
        #self.cmb_utype=ttk.Combobox(self.register_frame,font=("time new roman",15),state='readonly',justify=CENTER)
        #self.cmb_utype['values']=("Select","Admin","Employee")
        #self.cmb_utype.place(x=200,y=350,width=250)
        #self.cmb_utype.current(0)
        
        self.register_button = tk.Button(self.register_frame, text="Register",font=("time new roman",20,"bold"),cursor="hand2",bg="white",fg="black" ,command=self.register)
        self.register_button.place(x=250,y=390,width=150)#grid(row=7, column=0, columnspan=2, pady=20)

    def is_valid_email(self, email):
        # Basic email validation using regex
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def is_valid_password(self, password):
        # Password validation: At least 6 characters
        return len(password) >= 6

    def register(self):
        User_id = self.User_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        user_type = self.user_type_var.get()

        if not all([User_id, first_name, last_name, email, password, confirm_password, user_type]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            messagebox.showerror("Error","for Example:xyz@gmail.com")
            return

        if not self.is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            self.cursor.execute("INSERT INTO employees (User_id, first_name, last_name, email, password, access_level) VALUES (?, ?, ?, ?, ?, ?)",
                                (User_id, first_name, last_name, email, password, user_type))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.master.destroy()
            os.system("python login.py")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID  already exists.")#or Email 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    
       
    def login_window(self):
        self.master.destroy()
        os.system("python login.py")
        
if __name__ == "__main__":
    root = tk.Tk()
    registration_page = RegistrationPage(root)
    root.mainloop()
