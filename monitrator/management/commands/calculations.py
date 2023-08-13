from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, MenuHours, Report
import csv

class Command(BaseCommand):
    help = 'Calculate uptime for stores'

    def handle(self, *args, **options):
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)

        all_stores = Store.objects.all()
        data = []

        for store in all_stores:
            store_id = store.store_id
            total_active_time = timedelta(seconds=0)
            total_active_last_day = timedelta(seconds=0)
            total_active_last_week = timedelta(seconds=0)
            downtime_last_hour = timedelta(seconds=0)
            downtime_last_day = timedelta(seconds=0)
            downtime_last_week = timedelta(seconds=0)
            total_active_last_week_d = timedelta(seconds=0)

            business_hours = MenuHours.objects.filter(store_id=store_id)

            # Rest of your calculations...

            data.append([
                store_id,
                total_active_time.total_seconds() / 60,
                min(downtime_last_hour.total_seconds() / 60, 60),
                total_active_last_day.total_seconds() / 3600,
                downtime_last_day.total_seconds() / 3600,
                total_active_last_week.total_seconds() / 3600,
                168 - (total_active_last_week.total_seconds() / 3600)
            ])

        timestamp_str = now.strftime("%Y%m%d_%H%M%S")  # Generate a timestamp string
        csv_filename = f'store_metrics_{timestamp_str}.csv'  # Replace with your desired filename

        # Create a new Report instance with the generated report_id and status 'Running'
        report = Report.objects.create(report_id=timestamp_str, status='Running')

        with open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Rest of your CSV writing...

        # Update the Report instance with status 'Complete'
        report.status = 'Complete'
        report.save()

        self.stdout.write(self.style.SUCCESS(f"CSV file '{csv_filename}' created successfully."))
