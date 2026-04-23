import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import OTP

def test_otp_flow():
    # 1. Get or create test user
    user, created = User.objects.get_or_create(username='test_otp_user', email='test_otp@example.com')
    if created:
        user.set_password('testpass123')
        user.save()
    
    # 2. Create OTP
    code = "123456"
    OTP.objects.filter(user=user).delete()
    otp_obj = OTP.objects.create(user=user, code=code)
    
    print(f"Created OTP ID: {otp_obj.id}")
    print(f"Stored code (raw access): {otp_obj.code}")
    print(f"Type of otp_obj.code: {type(otp_obj.code)}")
    
    # 3. Verify logic mirroring views.py
    stored_code = str(otp_obj.code).strip()
    input_code = "123456".strip()
    
    print(f"Stored Code (str): '{stored_code}'")
    print(f"Input Code: '{input_code}'")
    print(f"Is Valid (method): {otp_obj.is_valid()}")
    print(f"Comparison Result: {stored_code == input_code}")
    
    if stored_code == input_code and otp_obj.is_valid():
        print("SUCCESS: OTP verified correctly in script.")
    else:
        print("FAILURE: OTP verification failed in script.")

if __name__ == "__main__":
    test_otp_flow()
