import datetime
import pytz
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from core.models import NewsAlert, Portfolio
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Send *all* stored news alerts to each user according to their portfolio holdings (ignores the 9am‑9am time window).'

    def handle(self, *args, **options):
        self.stdout.write('Starting full-news broadcast...')
        # Fetch **all** news alerts (no date filter)
        all_news = NewsAlert.objects.all()
        if not all_news.exists():
            self.stdout.write(self.style.WARNING('No NewsAlert records found in the database.'))
            return

        # Build a mapping of instrument_id -> list of alerts
        news_by_instrument = {}
        for news in all_news:
            news_by_instrument.setdefault(news.instrument_id, []).append(news)

        # Get all active users
        users = User.objects.filter(is_active=True).distinct()
        sent_count = 0
        for user in users:
            # Determine which instruments the user holds (quantity > 0)
            user_holdings = Portfolio.objects.filter(user=user, quantity__gt=0).values_list('instrument_id', flat=True)
            relevant_news = []
            for inst_id in user_holdings:
                relevant_news.extend(news_by_instrument.get(inst_id, []))

            if not relevant_news:
                continue  # nothing to send to this user

            # Render email using the same template as daily news (you may adjust as needed)
            context = {
                'user': user,
                'today': datetime.datetime.now(pytz.timezone('Asia/Kolkata')),
                'news_items': relevant_news,
                'site_url': getattr(settings, 'SITE_URL', 'https://foliux.com'),
            }
            html_message = render_to_string('emails/daily_portfolio_summary.html', context)
            plain_message = ''
            subject = f"Foliux – News Update for {user.get_full_name() or user.username}"
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Sent news to {user.email}'))
                sent_count += 1
            except Exception as e:
                self.stderr.write(f'Failed to send news to {user.email}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Finished. Sent news to {sent_count} users.'))
