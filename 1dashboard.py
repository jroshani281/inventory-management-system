import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class InventoryMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1350x700+0+0")#("1000x600")
        
        # Initialize database
        self.init_db()
        
        # Create GUI
        self.create_gui()
        
        # Load initial data
        self.load_data()
    
    def init_db(self):
        """Initialize the SQLite database and tables"""
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()    
        # Create tables if they don't exist     
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT,
                            gender TEXT,
                            date_of_birth INTEGER,
                            contact TEXT,
                            work_type TEXT,
                            address TEXT,
                            date_of_joining INTEGER,
                            salary INTEGER,
                            password TEXT NOT NULL 
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE
                            )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            category_id INTEGER,
                            stock INTEGER DEFAULT 0,
                            price REAL,
                            FOREIGN KEY (category_id) REFERENCES categories(id)
                            )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            contact TEXT,
                            email TEXT
                            )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER,
                            quantity INTEGER,
                            order_date TEXT,
                            status TEXT,
                            FOREIGN KEY (product_id) REFERENCES products(id)
                            )''')
        
       # self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        #                    id INTEGER PRIMARY KEY AUTOINCREMENT,
         #                   username TEXT UNIQUE NOT NULL,
         #                   password TEXT NOT NULL,
         #                   role TEXT
          #                  )''')
        
        self.conn.commit()
        
        # Insert some sample data if tables are empty
        
        self.conn.commit()
    def insert_sample_data(self):
        """Insert sample data if tables are empty"""
         # Check if employees table is empty
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        if self.cursor.fetchone()[0] == 0:
            employees = [
                ('Roshani Jain ', 'rjain@01.com', 'Female', '2005-05-15', '1234567890', 
                 'Full-time',  'NDB', '2020-01-10', 15000, 'password123'),
                ('neha patil', 'neha@example.com', 'Female', '1985-08-22', '9876543210',
                 'Part-time', 'Shahada', '2021-03-15', 10000, '12345678')
            ]
            for employee in employees:
                self.cursor.execute('''INSERT INTO employees 
                                    (name, email, gender, date_of_birth, contact, work_type, 
                                     address, date_of_joining, salary, password)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', employee)
        
        self.conn.commit()
         
        # Check if categories table is empty
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            categories = ['Electronic', 'Tech', 'Office']
            for category in categories:
                self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
        
        # Check if products table is empty
        self.cursor.execute("SELECT COUNT(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            products = [
                ('Monitor', 1, 10, 250),
                ('Screen', 1, 0, 350),
                ('PC', 2, 3, 800),
                ('RAM', 2, 2, 120),
                ('Keyboard', 1, 15, 50),
                ('Mouse', 1, 20, 30),
                ('Printer', 3, 8, 200),
                ('Desk', 3, 7, 150)
            ]
            for product in products:
                self.cursor.execute("INSERT INTO products (name, category_id, stock, price) VALUES (?, ?, ?, ?)", product)      
        self.conn.commit()
    
    def create_gui(self):
        """Create the main GUI layout"""
        # Create main container
        self.main_container = tk.Frame(self.root, bg='#f0f0f0')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.main_container, width=200, bg='#2c3e50')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Dashboard button
        self.dashboard_btn = tk.Button(self.sidebar, text="Dashboard", bg='#34495e', fg='white', 
                                      command=self.show_dashboard, padx=10, pady=5, width=15)
        self.dashboard_btn.pack(pady=(20, 5), padx=10)
        
        # Other menu buttons
        menu_items = [
            "Employees","Products", "Categories", "Orders", 
            "Suppliers", "Logout"
        ]
        
        for item in menu_items:
            btn = tk.Button(self.sidebar, text=item, bg='#34495e', fg='white', 
                           command=lambda i=item: self.show_page(i.lower()), 
                           padx=10, pady=5, width=15)
            btn.pack(pady=5, padx=10)
        
        # Main content area
        self.content = tk.Frame(self.main_container, bg='white')
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create pages
        self.pages = {}
        self.create_dashboard()
        self.create_employees_page()
        self.create_products_page()
        self.create_categories_page()
        self.create_orders_page()
        self.create_suppliers_page()
       
        
        # Show dashboard by default
        self.show_page('dashboard')
    
    def create_dashboard(self):
        """Create the dashboard page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['dashboard'] = page
        
        # Title
        title = tk.Label(page, text="Dashboard", font=('Helvetica', 16, 'bold'), bg='white')
        title.pack(pady=10, anchor='w', padx=20)
        
        # Stats frame
        stats_frame = tk.Frame(page, bg='white')
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Total Employees
        total_employees = tk.Frame(stats_frame, bg="#e3fdfb", width=200, height=100)
        total_employees.pack_propagate(False)
        total_employees.pack(side=tk.LEFT, padx=5)
        tk.Label(total_employees, text="Total Employees", bg="#e3fdfb", font=('Helvetica', 10)).pack(pady=(10, 5))
        self.total_employees_label = tk.Label(total_employees, text="0", bg="#e3fdfb", font=('Helvetica', 20, 'bold'))
        self.total_employees_label.pack()
        
        # Total Products
        total_products = tk.Frame(stats_frame, bg='#e3f2fd', width=200, height=100)
        total_products.pack_propagate(False)
        total_products.pack(side=tk.LEFT, padx=5)
        tk.Label(total_products, text="Total Products", bg='#e3f2fd', font=('Helvetica', 10)).pack(pady=(10, 5))
        self.total_products_label = tk.Label(total_products, text="0", bg='#e3f2fd', font=('Helvetica', 20, 'bold'))
        self.total_products_label.pack()
        
        # Total Stock
        total_stock = tk.Frame(stats_frame, bg='#e8f5e9', width=200, height=100)
        total_stock.pack_propagate(False)
        total_stock.pack(side=tk.LEFT, padx=5)
        tk.Label(total_stock, text="Total Stock", bg='#e8f5e9', font=('Helvetica', 10)).pack(pady=(10, 5))
        self.total_stock_label = tk.Label(total_stock, text="0", bg='#e8f5e9', font=('Helvetica', 20, 'bold'))
        self.total_stock_label.pack()
        
        # Orders Today
        orders_today = tk.Frame(stats_frame, bg='#fff3e0', width=200, height=100)
        orders_today.pack_propagate(False)
        orders_today.pack(side=tk.LEFT, padx=5)
        tk.Label(orders_today, text="Orders Today", bg='#fff3e0', font=('Helvetica', 10)).pack(pady=(10, 5))
        self.orders_today_label = tk.Label(orders_today, text="0", bg='#fff3e0', font=('Helvetica', 20, 'bold'))
        self.orders_today_label.pack()
        
        # Revenue
        revenue = tk.Frame(stats_frame, bg='#fce4ec', width=200, height=100)
        revenue.pack_propagate(False)
        revenue.pack(side=tk.LEFT, padx=5)
        tk.Label(revenue, text="Revenue", bg='#fce4ec', font=('Helvetica', 10)).pack(pady=(10, 5))
        self.revenue_label = tk.Label(revenue, text="$0", bg='#fce4ec', font=('Helvetica', 20, 'bold'))
        self.revenue_label.pack()
        
        # Lower section
        lower_frame = tk.Frame(page, bg='white')
        lower_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Out of stock frame
        out_of_stock_frame = tk.Frame(lower_frame, bg='white', bd=1, relief=tk.GROOVE)
        out_of_stock_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(out_of_stock_frame, text="Out of Stock Products", bg='white', font=('Helvetica', 12, 'bold')).pack(pady=5)
        self.out_of_stock_list = tk.Listbox(out_of_stock_frame, height=10)
        self.out_of_stock_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # Added .pack()
        
        # Highest sale product frame
        highest_sale_frame = tk.Frame(lower_frame, bg='white', bd=1, relief=tk.GROOVE)
        highest_sale_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(highest_sale_frame, text="Highest Sale Product", bg='white', font=('Helvetica', 12, 'bold')).pack(pady=5)
        self.highest_sale_label = tk.Label(highest_sale_frame, text="Name: -\nCategory: -\nUnits Sold: 0", 
                                          bg='white', justify=tk.LEFT)
        self.highest_sale_label.pack(pady=5)
        
        # Low stock frame
        low_stock_frame = tk.Frame(lower_frame, bg='white', bd=1, relief=tk.GROOVE)
        low_stock_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(low_stock_frame, text="Low Stock Products", bg='white', font=('Helvetica', 12, 'bold')).pack(pady=5)
        self.low_stock_list = tk.Listbox(low_stock_frame, height=10)
        self.low_stock_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # Added .pack()
        
    def create_employees_page(self):
        """Create the employees management page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['employees'] = page        
        # Title
        tk.Label(page, text="Employees Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)        
        # Toolbar
        toolbar = tk.Frame(page, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        tk.Button(toolbar, text="Add Employee", command=self.show_add_employee_dialog).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Edit Employee", command=self.show_edit_employee_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT)
        # Search
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT)
        tk.Label(search_frame, text="Search:", bg='white').pack(side=tk.LEFT)
        self.employee_search = tk.Entry(search_frame, width=30)
        self.employee_search.pack(side=tk.LEFT, padx=5)
        self.employee_search.bind('<KeyRelease>', self.search_employees)# Create tables if they don't exist
         # Employees table
        columns = ("id", "name", "email", "gender", "date_of_birth", "contact", "work_type", "address", "date_of_joining", "salary", "password")
        self.employees_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)
        for col in columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=100, anchor=tk.CENTER)        
        self.employees_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        # Scrollbar
        

    def create_products_page(self):
        """Create the products management page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['products'] = page      
        # Title
        tk.Label(page, text="Products Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)       
        # Toolbar
        toolbar = tk.Frame(page, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=5)       
        tk.Button(toolbar, text="Add Product", command=self.show_add_product_dialog).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Edit Product", command=self.show_edit_product_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT)       
        # Search
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT)
        tk.Label(search_frame, text="Search:", bg='white').pack(side=tk.LEFT)
        self.product_search = tk.Entry(search_frame, width=30)
        self.product_search.pack(side=tk.LEFT, padx=5)
        self.product_search.bind('<KeyRelease>', self.search_products)       
        # Products table
        columns = ("ID", "Name", "Category", "Stock", "Price")
        self.products_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100, anchor=tk.CENTER)        
        self.products_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)       
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.products_tree, orient="vertical", command=self.products_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.products_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_categories_page(self):
        """Create the categories management page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['categories'] = page
        
        # Title
        tk.Label(page, text="Categories Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)
        
        # Toolbar
        toolbar = tk.Frame(page, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(toolbar, text="Add Category", command=self.show_add_category_dialog).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Edit Category", command=self.show_edit_category_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Delete Category", command=self.delete_category).pack(side=tk.LEFT)
        
        # Categories table
        columns = ("ID", "Name")
        self.categories_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
            self.categories_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.categories_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_orders_page(self):
        """Create the orders management page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['orders'] = page
        
        # Title
        tk.Label(page, text="Orders Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)
        
        # Toolbar
        toolbar = tk.Frame(page, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(toolbar, text="Add Order", command=self.show_add_order_dialog).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Process Order", command=self.process_order).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Cancel Order", command=self.cancel_order).pack(side=tk.LEFT)
        
        # Orders table
        columns = ("ID", "Product", "Quantity", "Date", "Status")
        self.orders_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.orders_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_suppliers_page(self):
        """Create the suppliers management page"""
        page = tk.Frame(self.content, bg='white')
        self.pages['suppliers'] = page
        
        # Title
        tk.Label(page, text="Suppliers Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)
        
        # Toolbar
        toolbar = tk.Frame(page, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(toolbar, text="Add Supplier", command=self.show_add_supplier_dialog).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Edit Supplier", command=self.show_edit_supplier_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Delete Supplier", command=self.delete_supplier).pack(side=tk.LEFT)
        
        # Suppliers table
        columns = ("ID", "Name", "Contact", "Email")
        self.suppliers_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.suppliers_tree.heading(col, text=col)
            self.suppliers_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.suppliers_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
   # def create_users_page(self):
   #     """Create the users management page"""
    #    page = tk.Frame(self.content, bg='white')
     #   self.pages['users'] = page
        
     #   # Title
     #   tk.Label(page, text="Users Management", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)
        
     #   # Toolbar
     #   toolbar = tk.Frame(page, bg='white')
      #  toolbar.pack(fill=tk.X, padx=20, pady=5)
        
      #  tk.Button(toolbar, text="Add User", command=self.show_add_user_dialog).pack(side=tk.LEFT)
      #  tk.Button(toolbar, text="Edit User", command=self.show_edit_user_dialog).pack(side=tk.LEFT, padx=5)
      #  tk.Button(toolbar, text="Delete User", command=self.delete_user).pack(side=tk.LEFT)
        
        # Users table
      #  columns = ("ID", "Username", "Role")
      #  self.users_tree = ttk.Treeview(page, columns=columns, show='headings', height=15)
        
      #  for col in columns:
      #      self.users_tree.heading(col, text=col)
      #      self.users_tree.column(col, width=100, anchor=tk.CENTER)
        
      #  self.users_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    #def create_profile_page(self):
     #   """Create the profile page"""
      #  page = tk.Frame(self.content, bg='white')
       # self.pages['profile'] = page
        
        # Title
       # tk.Label(page, text="My Profile", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=10, anchor='w', padx=20)
        
        # Profile form
       # form = tk.Frame(page, bg='white')
       # form.pack(pady=20, padx=20, anchor='w')
        
      #  tk.Label(form, text="Username:", bg='white').grid(row=0, column=0, sticky='e', pady=5)
      #  self.profile_username = tk.Entry(form, width=30)
      #  self.profile_username.grid(row=0, column=1, padx=5, pady=5)
        
     #   tk.Label(form, text="Current Password:", bg='white').grid(row=1, column=0, sticky='e', pady=5)
     #   self.profile_current_password = tk.Entry(form, width=30, show='*')
     #   self.profile_current_password.grid(row=1, column=1, padx=5, pady=5)
        
      #  tk.Label(form, text="New Password:", bg='white').grid(row=2, column=0, sticky='e', pady=5)
       # self.profile_new_password = tk.Entry(form, width=30, show='*')
        #self.profile_new_password.grid(row=2, column=1, padx=5, pady=5)
        
      #  tk.Label(form, text="Confirm Password:", bg='white').grid(row=3, column=0, sticky='e', pady=5)
      #  self.profile_confirm_password = tk.Entry(form, width=30, show='*')
      #  self.profile_confirm_password.grid(row=3, column=1, padx=5, pady=5)
        
     #   tk.Button(form, text="Update Profile", command=self.update_profile).grid(row=4, column=1, pady=10, sticky='e')
    
    def show_page(self, page_name):
        """Show the selected page"""
        for page in self.pages.values():
            page.pack_forget()
        
        if page_name in self.pages:
            self.pages[page_name].pack(fill=tk.BOTH, expand=True)
            # Refresh data when page is shown
            if page_name == 'dashboard':
                self.load_dashboard_data()
            elif page_name == 'employees':
                self.load_employees_data()
            elif page_name == 'products':
                self.load_products_data()
            elif page_name == 'categories':
                self.load_categories_data()
            elif page_name == 'orders':
                self.load_orders_data()
            elif page_name == 'suppliers':
                self.load_suppliers_data()
           # elif page_name == 'users':
            #    self.load_users_data()
           # elif page_name == 'profile':
            #    self.load_profile_data()
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.show_page('dashboard')
    
    def load_data(self):
        """Load all initial data"""
        self.load_dashboard_data()
        self.load_employees_data()
        self.load_products_data()
        self.load_categories_data()
        self.load_orders_data()
        self.load_suppliers_data()
        #self.load_users_data()
    
    def load_dashboard_data(self):
        """Load data for the dashboard"""   
        # Total employees
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        total_employees = self.cursor.fetchone()[0]
        self.total_employees_label.config(text=str(total_employees))
        
        # Total products
        self.cursor.execute("SELECT COUNT(*) FROM products")
        total_products = self.cursor.fetchone()[0]
        self.total_products_label.config(text=str(total_products))
        
        # Total stock
        self.cursor.execute("SELECT SUM(stock) FROM products")
        total_stock = self.cursor.fetchone()[0] or 0
        self.total_stock_label.config(text=str(total_stock))
        
        # Orders today
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("SELECT COUNT(*) FROM orders WHERE order_date = ?", (today,))
        orders_today = self.cursor.fetchone()[0]
        self.orders_today_label.config(text=str(orders_today))
        
        # Revenue (simplified calculation)
        self.cursor.execute("""
            SELECT SUM(p.price * o.quantity) 
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            WHERE o.status = 'Completed'
        """)
        revenue = self.cursor.fetchone()[0] or 0
        self.revenue_label.config(text=f"${revenue:.2f}")
        
        # Out of stock products
        self.out_of_stock_list.delete(0, tk.END)
        self.cursor.execute("""
            SELECT p.name, c.name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.stock = 0
        """)
        for product, category in self.cursor.fetchall():
            self.out_of_stock_list.insert(tk.END, f"{product} ({category})")
        
        # Highest sale product
        self.cursor.execute("""
            SELECT p.name, c.name, SUM(o.quantity) as total_sold
            FROM orders o
            JOIN products p ON o.product_id = p.id
            JOIN categories c ON p.category_id = c.id
            WHERE o.status = 'Completed'
            GROUP BY p.id
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        result = self.cursor.fetchone()
        if result:
            name, category, total_sold = result
            self.highest_sale_label.config(text=f"Name: {name}\nCategory: {category}\nTotal Units Sold: {total_sold}")
        else:
            self.highest_sale_label.config(text="Name: -\nCategory: -\nUnits Sold: 0")
        
        # Low stock products (stock <= 3)
        self.low_stock_list.delete(0, tk.END)
        self.cursor.execute("""
            SELECT p.name, p.stock, c.name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.stock > 0 AND p.stock <= 3
            ORDER BY p.stock
        """)
        for name, stock, category in self.cursor.fetchall():
            self.low_stock_list.insert(tk.END, f"{name} - {stock} left ({category})")
            
    def load_employees_data(self):
        """Load employees data into the treeview"""
        for row in self.employees_tree.get_children():
            self.employees_tree.delete(row)
        self.cursor.execute("SELECT id, name, email, gender, date_of_birth, contact, work_type, address, date_of_joining, salary, password FROM employees ORDER BY name")        
        for row in self.cursor.fetchall():
            self.employees_tree.insert('', tk.END, values=row)            
    def load_products_data(self):
        """Load products data into the treeview"""
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)       
        self.cursor.execute("""
            SELECT p.id, p.name, c.name, p.stock, p.price
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY p.name
        """)        
        for row in self.cursor.fetchall():
            self.products_tree.insert('', tk.END, values=row)    
    def load_categories_data(self):
        """Load categories data into the treeview"""
        for row in self.categories_tree.get_children():
            self.categories_tree.delete(row)        
        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")       
        for row in self.cursor.fetchall():
            self.categories_tree.insert('', tk.END, values=row)
    def load_orders_data(self):
        """Load orders data into the treeview"""
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)    
        self.cursor.execute("""
            SELECT o.id, p.name, o.quantity, o.order_date, o.status
            FROM orders o
            JOIN products p ON o.product_id = p.id
            ORDER BY o.order_date DESC
        """)     
        for row in self.cursor.fetchall():
            self.orders_tree.insert('', tk.END, values=row)
    def load_suppliers_data(self):
        """Load suppliers data into the treeview"""
        for row in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(row)    
        self.cursor.execute("SELECT id, name, contact, email FROM suppliers ORDER BY name")     
        for row in self.cursor.fetchall():
            self.suppliers_tree.insert('', tk.END, values=row)
    
   # def load_users_data(self):
    #    """Load users data into the treeview"""
     #   for row in self.users_tree.get_children():
      #      self.users_tree.delete(row)
        
      #  self.cursor.execute("SELECT id, username, role FROM users ORDER BY username")
        
      #  for row in self.cursor.fetchall():
      #      self.users_tree.insert('', tk.END, values=row)
    
    #def load_profile_data(self):
     #   """Load current user's profile data"""
     #   # In a real app, you would load the logged-in user's data
      #  self.profile_username.delete(0, tk.END)
      #  self.profile_username.insert(0, "admin")  # Default for demo
      #  self.profile_current_password.delete(0, tk.END)
       # self.profile_new_password.delete(0, tk.END)
       # self.profile_confirm_password.delete(0, tk.END)
       
    def search_employees(self, event=None):
        """Search employees by name"""
        search_term = self.employee_search.get()
        for row in self.employees_tree.get_children():
            self.employees_tree.delete(row)  
        self.cursor.execute("""
            SELECT id, name, email,gender,date_of_birth,contact, work_type, salary,address,date_of_joining,salary,password
            FROM employees
            WHERE name LIKE ?
            ORDER BY name
        """, (f"%{search_term}%",))
        
        for row in self.cursor.fetchall():
            self.employees_tree.insert('', tk.END, values=row)
    def search_products(self, event=None):
        """Search products by name"""
        search_term = self.product_search.get()
        
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)
        
        self.cursor.execute("""
            SELECT p.id, p.name, c.name, p.stock, p.price
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE ?
            ORDER BY p.name
        """, (f"%{search_term}%",))
        
        for row in self.cursor.fetchall():
            self.products_tree.insert('', tk.END, values=row)
    def show_add_employee_dialog(self):
        """Show dialog to add a new employee"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Employee")
        dialog.geometry("500x500")
        
        # Form fields
        fields = [
            ("Name:", "entry"),
            ("Email:", "entry"),
            ("Gender:", "option", ["Male", "Female", "Other"]),
            ("Date of Birth:", "entry"),
            ("Contact:", "entry"),
            ("Work Type:", "option", ["Full-time", "Part-time"]),
            ("Address:", "entry"),
            ("Date of Joining:", "entry"),
            ("Salary:", "entry"),
            ("Password:", "entry", "*")
        ]
        
        self.employee_entries = {}
        for i, (label, field_type, *args) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            if field_type == "entry":
                show_char = args[0] if args else None
                entry = tk.Entry(dialog, width=30, show=show_char)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
                self.employee_entries[label.lower().replace(" ", "_").replace(":", "")] = entry
            elif field_type == "option":
                var = tk.StringVar(dialog)
                var.set(args[0][0])  # Set default to first option
                dropdown = ttk.Combobox(dialog, textvariable=var, values=args[0], state='readonly')
                dropdown.grid(row=i, column=1, padx=10, pady=5, sticky='w')
                self.employee_entries[label.lower().replace(" ", "_").replace(":", "")] = var
        
        def save_employee():
            # Get all field values
            data = {}
            for key, entry in self.employee_entries.items():
                if isinstance(entry, tk.StringVar):
                    data[key] = entry.get()
                else:
                    data[key] = entry.get()
            
            # Validate required fields
            if not data['name'] or not data['password']:
                messagebox.showerror("Error", "Name and Password are required!")
                return
            
            try:
                # Insert new employee
                self.cursor.execute('''INSERT INTO employees 
                                    (name, email, gender, date_of_birth, contact, work_type, 
                                      address, date_of_joining, salary, password)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (data['name'], data['email'], data['gender'], data['date_of_birth'],
                                     data['contact'], data['work_type'],  
                                     data['address'], data['date_of_joining'], data['salary'],
                                     data['password']))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Employee added successfully!")
                dialog.destroy()
                self.load_employees_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add employee: {str(e)}")
        
        tk.Button(dialog, text="Save", command=save_employee).grid(row=len(fields), column=1, pady=10, sticky='e')
          
    def show_edit_employee_dialog(self):
        """Show dialog to edit an employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee to edit!")
            return
        
        item = self.employees_tree.item(selected[0])
        id = item['values'][0]
        
        # Get employee details
        self.cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
        employee = self.cursor.fetchone()
        
        if not employee:
            messagebox.showerror("Error", "Employee not found!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Employee")
        dialog.geometry("500x500")
        
        # Form fields
        fields = [
            ("Name:", "entry", employee[1]),
            ("Email:", "entry", employee[2]),
            ("Gender:", "option", ["Male", "Female", "Other"], employee[3]),
            ("Date of Birth:", "entry", employee[4]),
            ("Contact:", "entry", employee[5]),
            ("Work Type:", "option", ["Full-time", "Part-time"], employee[6]),
            ("Address:", "entry", employee[7]),
            ("Date of Joining:", "entry", employee[8]),
            ("Salary:", "entry", employee[9]),
            ("Password:", "entry", "*", employee[10])
        ]
        
        self.employee_entries = {}
        for i, (label, field_type, *args) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            if field_type == "entry":
                initial_value = args[0]
                show_char = args[1] if len(args) > 1 else None
                entry = tk.Entry(dialog, width=30, show=show_char)
                entry.insert(0, initial_value)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
                self.employee_entries[label.lower().replace(" ", "_").replace(":", "")] = entry
            elif field_type == "option":
                options = args[0]
                initial_value = args[1]
                var = tk.StringVar(dialog)
                var.set(initial_value)
                dropdown = ttk.Combobox(dialog, textvariable=var, values=options, state='readonly')
                dropdown.grid(row=i, column=1, padx=10, pady=5, sticky='w')
                self.employee_entries[label.lower().replace(" ", "_").replace(":", "")] = var    
        def save_changes():
            # Get all field values
            data = {}
            for key, entry in self.employee_entries.items():
                if isinstance(entry, tk.StringVar):
                    data[key] = entry.get()
                else:
                    data[key] = entry.get()
            
            # Validate required fields
            if not data['name']:
                messagebox.showerror("Error", "Name is required!")
                return
            
            try:
                # Update employee
                self.cursor.execute('''UPDATE employees SET
                                    name=?, email=?, gender=?, date_of_birth=?, contact=?, 
                                    work_type=?, address=?, date_of_joining=?, 
                                    salary=?, password=?
                                    WHERE id=?''',
                                    (data['name'], data['email'], data['gender'], data['date_of_birth'],
                                     data['contact'], data['work_type'], 
                                     data['address'], data['date_of_joining'], data['salary'],
                                     data['password'], id))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Employee updated successfully!")
                dialog.destroy()
                self.load_employees_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
        
        tk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), column=1, pady=10, sticky='e') 
        
    def delete_employee(self):
        """Delete selected employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a employee to delete!")
            return
        
        item = self.employees_tree.item(selected[0])
        id, name, _, _, _, _, _, _, _, _ = item['values']
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {name}?"):
            self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Employee deleted successfully!")
            self.load_employees_data()
            self.load_dashboard_data()
             
    def show_add_product_dialog(self):
        """Show dialog to add a new product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Product Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()
        
        tk.Label(dialog, text="Category:").pack(pady=(10, 0))
        
        # Get categories for dropdown
        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        category_var = tk.StringVar(dialog)
        category_dropdown = ttk.Combobox(dialog, textvariable=category_var, values=category_names, state='readonly')
        category_dropdown.pack()
        if category_names:
            category_var.set(category_names[0])
        
        tk.Label(dialog, text="Initial Stock:").pack(pady=(10, 0))
        stock_entry = tk.Entry(dialog, width=30)
        stock_entry.pack()
        
        tk.Label(dialog, text="Price:").pack(pady=(10, 0))
        price_entry = tk.Entry(dialog, width=30)
        price_entry.pack()
        
        def save_product():
            name = name_entry.get()
            category_name = category_var.get()
            stock = stock_entry.get()
            price = price_entry.get()
            
            if not name or not category_name or not stock or not price:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                stock = int(stock)
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Stock must be an integer and price must be a number!")
                return
            
            # Get category ID
            category_id = None
            for cat in categories:
                if cat[1] == category_name:
                    category_id = cat[0]
                    break
            
            if not category_id:
                messagebox.showerror("Error", "Invalid category selected!")
                return
            
            # Insert new product
            self.cursor.execute(
                "INSERT INTO products (name, category_id, stock, price) VALUES (?, ?, ?, ?)",
                (name, category_id, stock, price)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", "Product added successfully!")
            dialog.destroy()
            self.load_products_data()
            self.load_dashboard_data()
        
        tk.Button(dialog, text="Save", command=save_product).pack(pady=20)
    
    def show_edit_product_dialog(self):
        """Show dialog to edit a product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to edit!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id, name, category, stock, price = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Product Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, name)
        name_entry.pack()
        
        tk.Label(dialog, text="Category:").pack(pady=(10, 0))
        
        # Get categories for dropdown
        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        category_var = tk.StringVar(dialog)
        category_dropdown = ttk.Combobox(dialog, textvariable=category_var, values=category_names, state='readonly')
        category_dropdown.pack()
        category_var.set(category)
        
        tk.Label(dialog, text="Stock:").pack(pady=(10, 0))
        stock_entry = tk.Entry(dialog, width=30)
        stock_entry.insert(0, stock)
        stock_entry.pack()
        
        tk.Label(dialog, text="Price:").pack(pady=(10, 0))
        price_entry = tk.Entry(dialog, width=30)
        price_entry.insert(0, price)
        price_entry.pack()
        
        def save_changes():
            new_name = name_entry.get()
            new_category = category_var.get()
            new_stock = stock_entry.get()
            new_price = price_entry.get()
            
            if not new_name or not new_category or not new_stock or not new_price:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                new_stock = int(new_stock)
                new_price = float(new_price)
            except ValueError:
                messagebox.showerror("Error", "Stock must be an integer and price must be a number!")
                return
            
            # Get category ID
            category_id = None
            for cat in categories:
                if cat[1] == new_category:
                    category_id = cat[0]
                    break
            
            if not category_id:
                messagebox.showerror("Error", "Invalid category selected!")
                return
            
            # Update product
            self.cursor.execute(
                "UPDATE products SET name=?, category_id=?, stock=?, price=? WHERE id=?",
                (new_name, category_id, new_stock, new_price, product_id)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", "Product updated successfully!")
            dialog.destroy()
            self.load_products_data()
            self.load_dashboard_data()
        
        tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=20)
    
    def delete_product(self):
        """Delete selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to delete!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id, name, _, _, _ = item['values']
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {name}?"):
            self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.load_products_data()
            self.load_dashboard_data()
    
    def show_add_category_dialog(self):
        """Show dialog to add a new category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Category")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Category Name:").pack(pady=(20, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack(pady=10)
        
        def save_category():
            name = name_entry.get()
            if not name:
                messagebox.showerror("Error", "Category name is required!")
                return
            
            try:
                self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
                self.conn.commit()
                messagebox.showinfo("Success", "Category added successfully!")
                dialog.destroy()
                self.load_categories_data()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Category with this name already exists.")
        
        tk.Button(dialog, text="Save", command=save_category).pack(pady=10)
    
    def show_edit_category_dialog(self):
        """Show dialog to edit a category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to edit!")
            return
        
        item = self.categories_tree.item(selected[0])
        category_id, name = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Category")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Category Name:").pack(pady=(20, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, name)
        name_entry.pack(pady=10)
        
        def save_changes():
            new_name = name_entry.get()
            
            if not new_name:
                messagebox.showerror("Error", "Category name is required!")
                return
            
            try:
                self.cursor.execute("UPDATE categories SET name=? WHERE id=?", (new_name, category_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Category updated successfully!")
                dialog.destroy()
                self.load_categories_data()
                self.load_products_data() # Product category names might need refreshing
                self.load_dashboard_data()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Category with this name already exists.")
        
        tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=10)
    
    def delete_category(self):
        """Delete selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to delete!")
            return
        
        item = self.categories_tree.item(selected[0])
        category_id, name = item['values']
        
        # Check if products are associated with this category
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE category_id = ?", (category_id,))
        product_count = self.cursor.fetchone()[0]
        
        if product_count > 0:
            messagebox.showerror("Error", f"Cannot delete category '{name}' because {product_count} products are associated with it. Please reassign or delete these products first.")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete category '{name}'?"):
            self.cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Category deleted successfully!")
            self.load_categories_data()
    
    def show_add_order_dialog(self):
        """Show dialog to add a new order"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Order")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="Product:").pack(pady=(10, 0))
        
        # Get products for dropdown
        self.cursor.execute("SELECT id, name, stock FROM products ORDER BY name")
        products = self.cursor.fetchall()
        product_names = [prod[1] for prod in products]
        product_var = tk.StringVar(dialog)
        product_dropdown = ttk.Combobox(dialog, textvariable=product_var, values=product_names, state='readonly')
        product_dropdown.pack()
        if product_names:
            product_var.set(product_names[0])
        
        tk.Label(dialog, text="Quantity:").pack(pady=(10, 0))
        quantity_entry = tk.Entry(dialog, width=30)
        quantity_entry.pack()
        
        tk.Label(dialog, text="Status:").pack(pady=(10, 0))
        status_var = tk.StringVar(dialog)
        status_dropdown = ttk.Combobox(dialog, textvariable=status_var, values=['Pending', 'Completed', 'Cancelled'], state='readonly')
        status_dropdown.pack()
        status_var.set("Pending")
        
        def save_order():
            product_name = product_var.get()
            quantity = quantity_entry.get()
            status = status_var.get()
            order_date = datetime.now().strftime('%Y-%m-%d')
            
            if not product_name or not quantity or not status:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showerror("Error", "Quantity must be a positive integer.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer!")
                return
            
            # Get product ID and current stock
            product_id = None
            current_stock = 0
            for prod in products:
                if prod[1] == product_name:
                    product_id = prod[0]
                    current_stock = prod[2]
                    break
            
            if not product_id:
                messagebox.showerror("Error", "Invalid product selected!")
                return
            
            if status == 'Completed' and quantity > current_stock:
                messagebox.showerror("Error", f"Not enough stock for {product_name}. Available: {current_stock}")
                return
            
            # Insert new order
            self.cursor.execute(
                "INSERT INTO orders (product_id, quantity, order_date, status) VALUES (?, ?, ?, ?)",
                (product_id, quantity, order_date, status)
            )
            
            # If order is completed, decrease product stock
            if status == 'Completed':
                self.cursor.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (quantity, product_id)
                )
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Order added successfully!")
            dialog.destroy()
            self.load_orders_data()
            self.load_products_data() # Stock might have changed
            self.load_dashboard_data()
        
        tk.Button(dialog, text="Save", command=save_order).pack(pady=20)
    
    def process_order(self):
        """Process selected order (change status to Completed and update stock)"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order to process!")
            return
        
        item = self.orders_tree.item(selected[0])
        order_id, product_name, quantity, _, status = item['values']
        
        if status == 'Completed':
            messagebox.showinfo("Info", "This order is already completed.")
            return
        
        if status == 'Cancelled':
            messagebox.showerror("Error", "Cannot process a cancelled order.")
            return
        
        # Get product ID and current stock
        self.cursor.execute("SELECT id, stock FROM products WHERE name = ?", (product_name,))
        product_info = self.cursor.fetchone()
        
        if not product_info:
            messagebox.showerror("Error", "Product not found for this order.")
            return
        
        product_id, current_stock = product_info
        
        if quantity > current_stock:
            messagebox.showerror("Error", f"Not enough stock for {product_name}. Available: {current_stock}")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to process order ID {order_id} ({product_name}, Quantity: {quantity})?"):
            self.cursor.execute("UPDATE orders SET status = 'Completed' WHERE id = ?", (order_id,))
            self.cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Order processed successfully!")
            self.load_orders_data()
            self.load_products_data()
            self.load_dashboard_data()
    
    def cancel_order(self):
        """Cancel selected order (change status to Cancelled)"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order to cancel!")
            return
        
        item = self.orders_tree.item(selected[0])
        order_id, product_name, quantity, _, status = item['values']
        
        if status == 'Cancelled':
            messagebox.showinfo("Info", "This order is already cancelled.")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to cancel order ID {order_id} ({product_name}, Quantity: {quantity})?"):
            self.cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE id = ?", (order_id,))
            
            # If a completed order is cancelled, return stock
            if status == 'Completed':
                self.cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
                product_id = self.cursor.fetchone()[0]
                self.cursor.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity, product_id))

            self.conn.commit()
            
            messagebox.showinfo("Success", "Order cancelled successfully!")
            self.load_orders_data()
            self.load_products_data() # Stock might have changed back
            self.load_dashboard_data()
            
    def show_add_supplier_dialog(self):
        """Show dialog to add a new supplier"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Supplier")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="Supplier Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()
        
        tk.Label(dialog, text="Contact Info:").pack(pady=(10, 0))
        contact_entry = tk.Entry(dialog, width=30)
        contact_entry.pack()
        
        tk.Label(dialog, text="Email:").pack(pady=(10, 0))
        email_entry = tk.Entry(dialog, width=30)
        email_entry.pack()
        
        def save_supplier():
            name = name_entry.get()
            contact = contact_entry.get()
            email = email_entry.get()
            
            if not name:
                messagebox.showerror("Error", "Supplier name is required!")
                return
            
            self.cursor.execute(
                "INSERT INTO suppliers (name, contact, email) VALUES (?, ?, ?)",
                (name, contact, email)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", "Supplier added successfully!")
            dialog.destroy()
            self.load_suppliers_data()
        
        tk.Button(dialog, text="Save", command=save_supplier).pack(pady=20)
    
    def show_edit_supplier_dialog(self):
        """Show dialog to edit a supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to edit!")
            return
        
        item = self.suppliers_tree.item(selected[0])
        supplier_id, name, contact, email = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Supplier")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="Supplier Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, name)
        name_entry.pack()
        
        tk.Label(dialog, text="Contact Info:").pack(pady=(10, 0))
        contact_entry = tk.Entry(dialog, width=30)
        contact_entry.insert(0, contact)
        contact_entry.pack()
        
        tk.Label(dialog, text="Email:").pack(pady=(10, 0))
        email_entry = tk.Entry(dialog, width=30)
        email_entry.insert(0, email)
        email_entry.pack()
        
        def save_changes():
            new_name = name_entry.get()
            new_contact = contact_entry.get()
            new_email = email_entry.get()
            
            if not new_name:
                messagebox.showerror("Error", "Supplier name is required!")
                return
            
            self.cursor.execute(
                "UPDATE suppliers SET name=?, contact=?, email=? WHERE id=?",
                (new_name, new_contact, new_email, supplier_id)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", "Supplier updated successfully!")
            dialog.destroy()
            self.load_suppliers_data()
        
        tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=20)
    
    def delete_supplier(self):
        """Delete selected supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return
        
        item = self.suppliers_tree.item(selected[0])
        supplier_id, name, _, _ = item['values']
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete supplier '{name}'?"):
            self.cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Supplier deleted successfully!")
            self.load_suppliers_data()
    
    #def show_add_user_dialog(self):
     #   """Show dialog to add a new user"""
      #  dialog = tk.Toplevel(self.root)
      #  dialog.title("Add New User")
      #  dialog.geometry("400x250")
        
       # tk.Label(dialog, text="Username:").pack(pady=(10, 0))
       # username_entry = tk.Entry(dialog, width=30)
        #username_entry.pack()
        
        #tk.Label(dialog, text="Password:").pack(pady=(10, 0))
        #password_entry = tk.Entry(dialog, width=30, show='*')
        #password_entry.pack()
        
        #tk.Label(dialog, text="Role:").pack(pady=(10, 0))
        #role_var = tk.StringVar(dialog)
        #role_dropdown = ttk.Combobox(dialog, textvariable=role_var, values=['Admin', 'Manager', 'Staff'], state='readonly')
        #role_dropdown.pack()
        #role_var.set("Staff")
        
        #def save_user():
         #   username = username_entry.get()
          #  password = password_entry.get()
          #  role = role_var.get()
            
           # if not username or not password or not role:
            #    messagebox.showerror("Error", "All fields are required!")
            #    return
            
            # In a real application, hash the password before storing
            #self.cursor.execute(
             #   "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              #  (username, password, role)
            #)
            #self.conn.commit()
            
            #messagebox.showinfo("Success", "User added successfully!")
            #dialog.destroy()
            #self.load_users_data()
        
        #tk.Button(dialog, text="Save", command=save_user).pack(pady=20)
    
    #def show_edit_user_dialog(self):
     #   """Show dialog to edit a user"""
      #  selected = self.users_tree.selection()
       # if not selected:
        #    messagebox.showerror("Error", "Please select a user to edit!")
         #   return
        
        #item = self.users_tree.item(selected[0])
        #user_id, username, role = item['values']
        
       # dialog = tk.Toplevel(self.root)
       # dialog.title("Edit User")
       # dialog.geometry("400x250")
        
       # tk.Label(dialog, text="Username:").pack(pady=(10, 0))
       # username_entry = tk.Entry(dialog, width=30)
       # username_entry.insert(0, username)
       # username_entry.pack()
        
       # tk.Label(dialog, text="New Password (leave blank to keep current):").pack(pady=(10, 0))
       # password_entry = tk.Entry(dialog, width=30, show='*')
       # password_entry.pack()
        
       # tk.Label(dialog, text="Role:").pack(pady=(10, 0))
       # role_var = tk.StringVar(dialog)
       # role_dropdown = ttk.Combobox(dialog, textvariable=role_var, values=['Admin', 'Manager', 'Staff'], state='readonly')
       # role_dropdown.pack()
       # role_var.set(role)
        
       # def save_changes():
       #     new_username = username_entry.get()
       #     new_password = password_entry.get()
        #    new_role = role_var.get()
            
         #   if not new_username or not new_role:
         #       messagebox.showerror("Error", "Username and Role are required!")
          #      return
            
          #  if new_password:
          #      # In a real application, hash the password before storing
           #     self.cursor.execute(
           #         "UPDATE users SET username=?, password=?, role=? WHERE id=?",
           #         (new_username, new_password, new_role, user_id)
            #    )
            #else:
             #   self.cursor.execute(
              #      "UPDATE users SET username=?, role=? WHERE id=?",
               #     (new_username, new_role, user_id)
               # )
            #self.conn.commit()
            
            #messagebox.showinfo("Success", "User updated successfully!")
            #dialog.destroy()
         #   self.load_users_data()
        #
        #tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=20)
        
    #def delete_user(self):
       # """Delete selected user"""
       #selected = self.users_tree.selection()
       # if not selected:
     #       messagebox.showerror("Error", "Please select a user to delete!")
          #  return
        
      #  item = self.users_tree.item(selected[0])
       # user_id, username, _ = item['values']
        
        #if messagebox.askyesno("Confirm", f"Are you sure you want to delete user '{username}'?"):
        #    self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        #    self.conn.commit()
            
        #    messagebox.showinfo("Success", "User deleted successfully!")
        #    self.load_users_data()
            
   # def update_profile(self):
    #    """Update user profile (username and password)"""
     #   username = self.profile_username.get()
      #  current_password = self.profile_current_password.get()
       # new_password = self.profile_new_password.get()
       # confirm_password = self.profile_confirm_password.get()
        
       # if not username:
       #     messagebox.showerror("Error", "Username cannot be empty.")
    #     return
            
        # In a real app, you'd verify current_password against stored hashed password
        # For this demo, let's assume 'admin' is the default user and password
       # if username == "admin" and current_password == "": # Simplistic check for demo
        #     pass
       # else:
        #    messagebox.showerror("Error", "Incorrect current password or username (for demo, username 'admin' and empty password works).")
           # return

        #if new_password:
         #   if new_password != confirm_password:
          #      messagebox.showerror("Error", "New password and confirm password do not match!")
          #      return
          #  # In a real app, hash new_password before updating
          #  # self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_password, username))
           # messagebox.showinfo("Success", "Password updated successfully!")
        
        # Update username if it changed
        # self.cursor.execute("UPDATE users SET username=? WHERE id=?", (username, current_user_id)) # Needs current_user_id
        
     #   messagebox.showinfo("Success", "Profile updated successfully!")
      #  self.load_profile_data() # Refresh form
    
    #def on_closing(self):
     #   """Handle window closing event"""
      #  if messagebox.askokcancel("Quit", "Do you want to quit?"):
       #     self.conn.close()
        #    self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryMS(root)
    root.protocol("WM_DELETE_WINDOW")#app.on_closing
    root.mainloop()