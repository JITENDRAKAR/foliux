import sqlite3
import os

db_path = r'G:\My Drive\NPITS\db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in NPITS: {tables}")
    conn.close()
else:
    print("NPITS database not found.")
