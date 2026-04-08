
import os
import django
import sys
from django.db import connection, transaction
from decimal import Decimal

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.models import (
    Profile, OTP, SignupOTP, Loan, LoanPayment, FixedAsset
)

def encrypt_table(model_class, fields):
    print(f"Encrypting {model_class.__name__}...")
    updated_count = 0
    for obj in model_class.objects.all():
        needs_save = False
        for field in fields:
            val = getattr(obj, field)
            # If we can read it, it's either plaintext or already encrypted (and decrypted by Django)
            # When we .save(), Django will encrypt it.
            # We want to force a save if the DB currently holds plaintext.
            # To detect if DB holds plaintext for THIS specific object:
            with connection.cursor() as cursor:
                table_name = model_class._meta.db_table
                cursor.execute(f"SELECT {field} FROM {table_name} WHERE id=%s", [obj.id])
                raw_val = cursor.fetchone()[0]
                
                if raw_val and not str(raw_val).startswith('gAAAA'):
                    needs_save = True
                    break
        
        if needs_save:
            obj.save()
            updated_count += 1
            
    print(f"  Updated {updated_count} rows.")

def run():
    try:
        with transaction.atomic():
            encrypt_table(Profile, ['full_name', 'mobile_number', 'date_of_birth', 'gender'])
            encrypt_table(OTP, ['code'])
            encrypt_table(SignupOTP, ['email', 'code'])
            encrypt_table(Loan, ['bank_name', 'loan_amount', 'interest_rate', 'emi_amount'])
            encrypt_table(LoanPayment, ['amount', 'principal_component', 'interest_component'])
            encrypt_table(FixedAsset, ['instrument_name', 'invested_amount', 'interest_rate'])
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()
