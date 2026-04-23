import os
import MySQLdb
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

db_name = os.environ.get("DB_NAME", "FOLIUX")
db_user = os.environ.get("DB_USER", "foliux")
db_password = os.environ.get("DB_PASSWORD", "Test@123")
db_host = os.environ.get("DB_HOST", "158.220.101.59")
db_port = int(os.environ.get("DB_PORT", "3306"))

print(f"Attempting to connect to {db_host}:{db_port}...")
try:
    conn = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        db=db_name,
        port=db_port,
        connect_timeout=10
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
