import sqlite3

conn = sqlite3.connect('employee_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        access_level TEXT NOT NULL,
        user_id TEXT UNIQUE NOT NULL
    )
''')

conn.commit()
conn.close()