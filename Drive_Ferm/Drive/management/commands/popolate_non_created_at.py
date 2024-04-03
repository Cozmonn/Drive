from django.core.management.base import BaseCommand
from django.utils import timezone
from Drive.models import Product
import random
from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Populates the created_at field for existing Product instances with a random date'

    def handle(self, *args, **kwargs):
        # Define the time range for the random date
        days_back = 365 * 5  # for example, up to 5 years back

        for product in Product.objects.filter(created_at__isnull=True):
            # Generate a random number of days to subtract
            random_days_back = random.randrange(days_back)
            # Generate a random datetime within the last 5 years
            random_date = timezone.now() - timedelta(days=random_days_back)
            # Set this random datetime to the product's created_at
            product.created_at = random_date
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {product} with date {random_date}'))
