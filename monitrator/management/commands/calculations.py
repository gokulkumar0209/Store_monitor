from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, StoreStatus, MenuHours, StoreMetrics
import csv

class Command(BaseCommand):
    help = 'Calculate uptime and downtime for all stores'

    def handle(self, *args, **options):
        now = datetime.utcnow()

        all_stores = Store.objects.all()

        for store in all_stores:
            store_id = store.store_id

            business_hours = MenuHours.objects.filter(store_id=store_id)

            total_active = timedelta()  # Initialize total active time
            total_active_last_day = timedelta(seconds=0)
            total_active_last_week = timedelta(seconds=0)
            downtime_last_hour = 0  # Initialize downtime_last_hour

            for business_hour in business_hours:
                start_time_local = business_hour.start_time_local
                end_time_local = business_hour.end_time_local

                start_datetime_local = datetime.combine(datetime.today(), start_time_local)
                end_datetime_local = datetime.combine(datetime.today(), end_time_local)

                if start_datetime_local <= now <= end_datetime_local:
                    active = min(now, end_datetime_local) - max(start_datetime_local, last_hour)
                    total_active += active
                    downtime_last_hour = (3600 - total_active.total_seconds())

                if last_day < start_datetime_local <= now:
                    uptime_last_day = now - start_datetime_local
                    if now > end_datetime_local:
                        downtime_last_day = now - end_datetime_local
                        active_last_day = uptime_last_day - downtime_last_day
                    else:
                        active_last_day = now - uptime_last_day
                    total_active_last_day += active_last_day
                    downtime_last_day = (24 * 3600) - total_active_last_day.total_seconds()

                if last_week < start_datetime_local <= now:
                    uptime_last_week = now - start_datetime_local
                    if now > end_datetime_local:
                        downtime_last_week = now - end_datetime_local
                        active_last_week = uptime_last_week - downtime_last_week
                    else:
                        active_last_week = now - uptime_last_week
                    total_active_last_week += active_last_week

            downtime_last_week = (7 * 24 * 3600) - total_active_last_week.total_seconds()

            metrics = StoreMetrics(
                store=store,
                uptime_last_hour=total_active.total_seconds() / 60,  # Convert to minutes
                uptime_last_day=total_active_last_day.total_seconds() / 3600,  # Convert to hours
                uptime_last_week=total_active_last_week.total_seconds() / 3600,  # Convert to hours
                downtime_last_hour=downtime_last_hour / 60,  # Convert to minutes
                downtime_last_day=downtime_last_day / 3600,  # Convert to hours
                downtime_last_week=downtime_last_week / 3600  # Convert to hours
            )
            metrics.save()

            self.stdout.write(f"Store ID: {store_id}")
            self.stdout.write(f"Uptime Last Hour: {total_active.total_seconds() / 60:.2f} minutes")
            self.stdout.write(f"Uptime Last Day: {total_active_last_day.total_seconds() / 3600:.2f} hours")
            self.stdout.write(f"Uptime Last Week: {total_active_last_week.total_seconds() / 3600:.2f} hours")
            self.stdout.write(f"Downtime Last Hour: {downtime_last_hour / 60:.2f} minutes")
            self.stdout.write(f"Downtime Last Day: {downtime_last_day / 3600:.2f} hours")
            self.stdout.write(f"Downtime Last Week: {downtime_last_week / 3600:.2f} hours")
            self.stdout.write("-" * 50)

        # Define CSV filename
        csv_filename = "store_metrics.csv"

        # Write data to CSV file
        with open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "Store ID", "Uptime Last Hour (minutes)", "Uptime Last Day (hours)",
                "Uptime Last Week (hours)", "Downtime Last Hour (minutes)",
                "Downtime Last Day (hours)", "Downtime Last Week (hours)"
            ])
            for store in StoreMetrics.objects.all():
                csv_writer.writerow([
                    store.store.store_id, store.uptime_last_hour, store.uptime_last_day,
                    store.uptime_last_week, store.downtime_last_hour,
                    store.downtime_last_day, store.downtime_last_week
                ])

        self.stdout.write(f"CSV file '{csv_filename}' created successfully.")
