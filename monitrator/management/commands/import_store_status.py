from django.core.management.base import BaseCommand
from monitrator.models import StoreStatus
import csv
from datetime import datetime
from decimal import Decimal

class Command(BaseCommand):
    help = 'Import store statuses from CSV file'
    print("Hi")

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']        
        with open(csv_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            i = 0
            for row in csv_reader:
                print(row)
                i += 1
                if i == 4000:
                    break
                store_id = int(Decimal(row['store_id']))
                status = row['status']
                timestamp_utc = datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S.%f %Z')

                store_status = StoreStatus(
                    store_id=store_id,
                    status=status,
                    timestamp_utc=timestamp_utc
                )
                store_status.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully imported store status for store {store_id}'))
