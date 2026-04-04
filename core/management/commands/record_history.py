from django.core.management.base import BaseCommand
from core.utils import record_all_portfolio_history
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Record today\'s portfolio valuation history for all users'

    def handle(self, *args, **options):
        self.stdout.write("Recording portfolio value snapshots for all users...")
        try:
            count = record_all_portfolio_history()
            self.stdout.write(self.style.SUCCESS(f"Successfully recorded history for {count} users."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to record history: {e}"))
