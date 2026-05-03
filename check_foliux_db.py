import sqlite3
import os

db_path = r'G:\My Drive\foliux\db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in Foliux Local: {tables}")
    if ('core_ipo',) in tables:
        cursor.execute("SELECT name FROM core_ipo WHERE name LIKE '%AMBA%';")
        print(f"AMBA matches: {cursor.fetchall()}")
    conn.close()
else:
    print("Foliux Local database not found.")
