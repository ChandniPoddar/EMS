import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "employees.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# EMPLOYEE TABLE
cursor.execute("""
CREATE TABLE employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    role TEXT,
    salary INTEGER
)
""")

# ADMIN TABLE
cursor.execute("""
CREATE TABLE admin (
    username TEXT,
    password TEXT
)
""")

# INSERT DEFAULT ADMIN
cursor.execute(
    "INSERT INTO admin (username, password) VALUES (?, ?)",
    ("admin", "admin123")
)

conn.commit()
conn.close()

print("Database created with admin table")
