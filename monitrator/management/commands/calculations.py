from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, StoreStatus, MenuHours

class Command(BaseCommand):
    help = 'Calculate uptime and downtime for all stores'

    def handle(self, *args, **options):
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)

        all_stores = Store.objects.all()
        for store in all_stores:
            store_id = store.store_id

            # Get all active status records for the store
            # active_statuses = StoreStatus.objects.filter(store_id=store_id, status='active')
            # print(active_statuses)
            business_hours=Men
        #     # Calculate uptime and downtime for the last hour
        #     active_last_hour = active_statuses.filter(timestamp_utc__gte=last_hour)
        #     uptime_last_hour = active_last_hour.count()
        #     downtime_last_hour = 60 - uptime_last_hour

        #     # Calculate uptime for the last day
        #     active_last_day = active_statuses.filter(timestamp_utc__gte=last_day)
        #     uptime_last_day = active_last_day.count()
            
        #     # Calculate uptime for the last week
        #     uptime_last_week = active_statuses.count()

        #     # Calculate downtime for the last day and week
        #     downtime_last_day = 24 - uptime_last_day
        #     downtime_last_week = 7 - uptime_last_week

            # self.stdout.write(f"Store ID: {store_id}")
            # self.stdout.write(f"Uptime Last Hour: {uptime_last_hour} minutes")
            # self.stdout.write(f"Uptime Last Day: {uptime_last_day} hours")
            # self.stdout.write(f"Uptime Last Week: {uptime_last_week} hours")
            # self.stdout.write(f"Downtime Last Hour: {downtime_last_hour} minutes")
            # self.stdout.write(f"Downtime Last Day: {downtime_last_day} hours")
            # self.stdout.write(f"Downtime Last Week: {downtime_last_week} hours")
            # self.stdout.write("-" * 50)