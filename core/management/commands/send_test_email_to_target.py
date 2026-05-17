import datetime
import pytz
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from core.models import NewsAlert
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Send a test news email to a specific address to verify SMTP configuration.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Target email address to receive the test message.'
        )

    def handle(self, *args, **options):
        target_email = options['email']
        # Build a simple test email using the same 9am‑9am window logic
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(ist)
        end_dt = now.replace(hour=9, minute=0, second=0, microsecond=0)
        start_dt = end_dt - datetime.timedelta(days=1)
        news_items = NewsAlert.objects.filter(news_date__gte=start_dt.date(), news_date__lte=end_dt.date())[:3]

        subject = f"Foliux: Test News Email – {now.strftime('%d %b %Y')}"
        content = "<h2>Test News Email</h2>"
        if news_items:
            content += "<p>Sample news from the last 24 h (9 am‑9 am) window:</p>"
            for item in news_items:
                content += f"<div style='margin-bottom:15px;'><h3>{item.instrument.symbol}: {item.title}</h3>"
                content += f"<p>{item.summary[:200]}...</p>"
                if item.url:
                    content += f"<a href='{item.url}' style='color:#3498db;'>Read Full Story</a>"
                content += "</div>"
        else:
            content += "<p>This is a test email to verify that your SMTP settings are correct.</p>"

        try:
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[target_email],
                html_message=content,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Test email sent to {target_email}'))
        except Exception as e:
            self.stderr.write(f'Failed to send test email: {e}')
