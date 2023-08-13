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
            status = StoreStatus.objects.filter(store_id=store_id)

            total_active = timedelta()  # Initialize total active time
            hours_in_day = 0
            day_max = -1

            for business_hour in business_hours:
                day = business_hour.day
                day_max = max(day_max, day)
                start_time_local = datetime.combine(datetime.today(), business_hour.start_time_local)
                end_time_local = datetime.combine(datetime.today(), business_hour.end_time_local)

                if end_time_local < start_time_local:
                    # Handle case where end time is before start time (crosses midnight)
                    end_time_local += timedelta(days=1)

                active_duration = end_time_local - start_time_local  # Calculate active duration

                # Calculate total active time for this business hour
                active_duration_total_seconds = active_duration.total_seconds()
                active_duration_total_hours = active_duration_total_seconds / 3600  # Convert seconds to hours

                if day == day_max:
                    hours_in_day = active_duration_total_hours

                total_active += timedelta(hours=active_duration_total_hours)

            # Calculate other metrics
            uptime_last_hour = hours_in_day * 60
            uptime_last_day = total_active.total_seconds() / 3600
            uptime_last_week = total_active.total_seconds() / 3600

            # Calculate downtime for the last hour (considering time passed within the current hour)
            downtime_last_hour = (60 - uptime_last_hour) if hours_in_day >= 1 else 60

            downtime_last_day = 24 - uptime_last_day  # Correct calculation
            downtime_last_week = 7 * 24 - uptime_last_week  # Correct calculation
            metrics = StoreMetrics(
                store=store,
                uptime_last_hour=uptime_last_hour,
                uptime_last_day=uptime_last_day,
                uptime_last_week=uptime_last_week,
                downtime_last_hour=downtime_last_hour,
                downtime_last_day=downtime_last_day,
                downtime_last_week=downtime_last_week
            )
            metrics.save()

            self.stdout.write(f"Store ID: {store_id}")
            self.stdout.write(f"Uptime Last Hour: {uptime_last_hour:.2f} minutes")
            self.stdout.write(f"Uptime Last Day: {uptime_last_day:.2f} hours")
            self.stdout.write(f"Uptime Last Week: {uptime_last_week:.2f} hours")
            self.stdout.write(f"Downtime Last Hour: {downtime_last_hour:.2f} minutes")
            self.stdout.write(f"Downtime Last Day: {downtime_last_day:.2f} hours")
            self.stdout.write(f"Downtime Last Week: {downtime_last_week:.2f} hours")
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
