from django.core.management.base import BaseCommand
from django.utils import timezone
from Drive.models import Product
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Updates each product with a random previous date for created_at'

    def handle(self, *args, **kwargs):
        # Define the range of days in the past you want the random date to be selected from
        days_back = 365 * 5  # Example: within the last 5 years

        for product in Product.objects.all():
            random_days_back = random.randint(1, days_back)
            random_date = timezone.now() - timedelta(days=random_days_back)
            
            product.created_at = random_date
            product.save()

            self.stdout.write(self.style.SUCCESS(f'Updated {product.id}: created_at set to {random_date}'))
