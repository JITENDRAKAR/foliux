import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.models import OTP

otp = OTP.objects.order_by('-created_at').first()
if otp:
    print(f"ID: {otp.id}")
    print(f"User: {otp.user.username}")
    print(f"Code (Decrypted): {otp.code}")
    print(f"Created At: {otp.created_at}")
    
    # Check raw value in DB to see truncation
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT code FROM core_otp WHERE id = %s", [otp.id])
        row = cursor.fetchone()
        if row:
            raw_code = row[0]
            print(f"Raw Code in DB: {raw_code}")
            print(f"Length in DB: {len(raw_code)}")
else:
    print("No OTP found.")
