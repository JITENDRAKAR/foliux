import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    print(f"Databases: {databases}")
    for db in databases:
        db_name = db[0]
        if db_name in ['information_schema', 'mysql', 'performance_schema', 'sys']:
            continue
        print(f"Checking database: {db_name}")
        cursor.execute(f"USE {db_name};")
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        if 'core_ipo' in tables:
            cursor.execute("SELECT name FROM core_ipo WHERE name LIKE '%AMBA%';")
            res = cursor.fetchall()
            if res:
                print(f"!!! FOUND IN {db_name}: {res}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
