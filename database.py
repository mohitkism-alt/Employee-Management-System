import sqlite3
import pandas as pd

DB = "employee_v2.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS employees (id TEXT PRIMARY KEY, name TEXT, phone TEXT, role TEXT, gender TEXT, salary REAL)")
    conn.commit()
    conn.close()

def fetch():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()
    return df

def insert(data):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO employees VALUES(?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()

def update(data):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE employees SET name=?, phone=?, role=?, gender=?, salary=? WHERE id=?", (data[1], data[2], data[3], data[4], data[5], data[0]))
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()