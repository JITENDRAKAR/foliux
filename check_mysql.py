import mysql.connector
import os

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="foliux"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, advise FROM core_ipo WHERE name LIKE '%AMBA%';")
    results = cursor.fetchall()
    print(f"Found in Local MySQL: {results}")
    conn.close()
except Exception as e:
    print(f"Error connecting to local MySQL: {e}")
