import sqlite3
try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM core_ipo")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} IPOs in SQLite.")
    for row in rows:
        print(row)
    conn.close()
except Exception as e:
    print(f"Error: {e}")
