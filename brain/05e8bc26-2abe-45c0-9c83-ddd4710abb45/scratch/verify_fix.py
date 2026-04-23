import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_advisory.settings')
django.setup()

from core.utils import get_recommendations
from core.models import User, Portfolio, Instrument

def verify():
    # Pick a user
    user = User.objects.first()
    if not user:
        print("No user found.")
        return

    print(f"Testing for user: {user.username}")
    
    recommendations, _, _ = get_recommendations(user)
    
    non_portfolio_items = [r for r in recommendations if not r.get('in_portfolio')]
    
    if not non_portfolio_items:
        print("No non-portfolio recommendations found. This might be normal if no strategies are active or no P&L exists.")
        return

    print(f"Found {len(non_portfolio_items)} non-portfolio recommendations.")
    
    count_nonzero = 0
    for r in non_portfolio_items:
        sym = r['symbol']
        pct = r.get('day_change_pct', 0)
        day_delta = r.get('day_change', 0)
        
        # We expect day_change to be 0 (because quantity is 0)
        # We expect day_change_pct to be non-zero if the instrument has price change data
        if pct != 0:
            count_nonzero += 1
            print(f"Symbol: {sym}, Day Delta: {day_delta}, Chg %: {pct}%")
            if count_nonzero >= 5: break

    if count_nonzero > 0:
        print(f"Success: Found {count_nonzero} items with non-zero Chg %.")
    else:
        print("Verification: No non-zero Chg % found. This could be because Instrument.price_change is 0 for all recommended stocks.")

if __name__ == "__main__":
    verify()
