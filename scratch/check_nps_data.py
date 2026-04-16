import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.models import NPSPortfolio, NPSFund
from decimal import Decimal

print("NPS Portfolio Check:")
portfolios = NPSPortfolio.objects.filter(units__gt=0)
if not portfolios.exists():
    print("No NPS holdings found.")
else:
    for p in portfolios:
        print(f"User: {p.user.username}, Fund: {p.fund.name}, Units: {p.units}, NAV: {p.fund.nav}, Current Val: {p.current_value}")

print("\nNPS Funds Check:")
for f in NPSFund.objects.all():
    print(f"Fund: {f.name}, NAV: {f.nav}")
