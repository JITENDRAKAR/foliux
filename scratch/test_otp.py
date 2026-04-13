import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.models import OTP, User

user = User.objects.first()
if user:
    OTP.objects.filter(user=user).delete()
    code = "123456"
    OTP.objects.create(user=user, code=code)
    
    # Try to filter
    otp = OTP.objects.filter(user=user, code=code).first()
    if otp:
        print(f"SUCCESS: Found OTP with code {code}")
    else:
        print(f"FAILURE: Could not find OTP with code {code}")
        # Let's see what's in the DB
        all_otps = OTP.objects.filter(user=user)
        for o in all_otps:
            print(f"Stored code (decrypted): {o.code}")
else:
    print("No user found")
