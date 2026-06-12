#  Inventory Management System

A desktop-based **Inventory Management System** built with **Python**, **Tkinter**, and **SQLite**. Designed for small retail or warehouse businesses to manage employees, sales, billing, and inventory through a clean, role-based GUI.

---

##  Features

-  **Role-Based Login** — Separate access for **Admin** and **Employee** accounts
-  **Employee Registration** — Add new staff with validated email & password
-  **Billing System** — Generate and save customer invoices
-  **Sales Tracking** — Search and view past invoices by invoice number
-  **Admin Dashboard** — Centralized control panel for managing inventory & employees
-  **SQLite Database** — Lightweight, file-based data storage

---

##  Tech Stack

| Component   | Technology |
|-------------|------------|
| Language    | Python 3.12 |
| GUI         | Tkinter, Pillow (PIL) |
| Database    | SQLite3 |
| Architecture| Multi-file, modular |

---

##  Project Structure

```
Inventory_Management_System/
├── login.py            # Login screen & authentication
├── register.py         # New employee registration
├── dashboard.py         # Admin dashboard
├── billing.py           # Billing / invoice generation
├── sales.py             # Sales & invoice search
├── database_setup.py    # Initializes SQLite database
├── employee_data.db     # Employee records
├── inventory.db         # Inventory data
├── ims.db               # Application database
├── bill/                # Saved invoice text files
└── image/               # UI images & icons
```

---

##  Getting Started

### Prerequisites
- Python 3.10+
- Pillow library

```bash
pip install pillow
```

### Setup & Run

1. Clone the repository
```bash
git clone https://github.com/jroshani281/inventory-management-system.git
cd inventory-management-system
```

2. Initialize the database
```bash
python database_setup.py
```

3. Launch the application
```bash
python login.py
```

---

##  User Roles

| Role     | Access |
|----------|--------|
| **Admin**    | Full dashboard — manage inventory, employees, sales |
| **Employee** | Billing screen — generate customer invoices |

---


---

##  Contributing

Contributions, issues, and feature requests are welcome!

---

##  License

This project is open source and available for educational use.

---

##  Author

**[jroshani281](https://github.com/jroshani281)**