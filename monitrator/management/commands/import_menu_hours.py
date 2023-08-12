import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from monitrator.models import Store, MenuHours, Timezone

class Command(BaseCommand):
    help = 'Import menu hours and timezone data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('menu_hours_csv_file', type=str, help='Path to the menu_hours CSV file')
        parser.add_argument('timezone_csv_file', type=str, help='Path to the timezone CSV file')

    def handle(self, *args, **kwargs):
        menu_hours_csv_file = kwargs['menu_hours_csv_file']
        timezone_csv_file = kwargs['timezone_csv_file']

        # Process the menu_hours CSV file
        with open(menu_hours_csv_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            i = 0
            for row in csv_reader:
                i += 1
                if i == 2500:
                    break

                # Extract store_id from the menu_hours CSV
                store_id = int(Decimal(row['store_id']))

                # Create or get Store instance
                store, created = Store.objects.get_or_create(store_id=store_id)

                # Process MenuHours here
                day_of_week = int(row['day'])
                start_time_local = datetime.strptime(row['start_time_local'], '%H:%M:%S').time()
                end_time_local = datetime.strptime(row['end_time_local'], '%H:%M:%S').time()

                menu_hours = MenuHours(
                    store=store,
                    day=day_of_week,
                    start_time_local=start_time_local,
                    end_time_local=end_time_local
                )
                menu_hours.save()

        # Process the timezone CSV file
        with open(timezone_csv_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            i=0
            for row in csv_reader:
                # Extract store_id and timezone_str from the timezone CSV
                
                store_id = int(Decimal(row['store_id']))
                timezone_str = row['timezone_str']

                # Associate the timezone with the Store instance
                try:
                    store = Store.objects.get(store_id=store_id)
                    timezone = Timezone(store=store, timezone_str=timezone_str)
                    timezone.save()
                except Store.DoesNotExist:
                    # Handle missing Store instance if needed
                    pass

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

