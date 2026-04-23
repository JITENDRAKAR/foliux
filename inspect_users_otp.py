import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import OTP

print("USERS:")
for user in User.objects.all():
    print(f"- {user.username} ({user.email})")

print("\nOTPs:")
for otp in OTP.objects.all().order_by('-created_at'):
    print(f"- User: {otp.user.username}, Created: {otp.created_at}, Code (Decrypted): {otp.code}")
