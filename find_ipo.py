import sqlite3
import os

db_path = r'G:\My Drive\NPITS\db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, advise FROM core_ipo WHERE name LIKE '%AMBAAUTO%';")
    results = cursor.fetchall()
    print(f"Found in NPITS: {results}")
    conn.close()
else:
    print("NPITS database not found.")
