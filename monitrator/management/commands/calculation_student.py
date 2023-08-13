from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, MenuHours

class Command(BaseCommand):
    help = 'Calculate uptime for stores'

    def handle(self, *args, **options):
        now = datetime.utcnow()
        last_hour = now - timedelta(minutes=60)  # Convert last hour to minutes
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)

        all_stores = Store.objects.all()

        for store in all_stores:
            store_id = store.store_id
            total_active_time = 0  # Initialize total active time
            total_active_last_day = timedelta(seconds=0)
            total_active_last_week = timedelta(seconds=0)
            downtime_last_hour = 0  # Initialize downtime_last_hour

            business_hours = MenuHours.objects.filter(store_id=store_id)

            for business_hour in business_hours:
                start_time_local = business_hour.start_time_local
                end_time_local = business_hour.end_time_local

                start_datetime_local = datetime.combine(datetime.today(), start_time_local)
                end_datetime_local = datetime.combine(datetime.today(), end_time_local)

                if start_datetime_local <= now <= end_datetime_local:
                    active = min(now, end_datetime_local) - max(start_datetime_local, last_hour)
                    total_active_time += active.total_seconds()
                    downtime_last_hour = (3600 - total_active_time)

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

            print(f"Store ID: {store_id}, Total Active Time (last hour): {total_active_time / 60:.2f} minutes")
            print(f"Downtime Last Hour: {downtime_last_hour / 60:.2f} minutes")
            print(f"Total Active Time (last day): {total_active_last_day.total_seconds() / 3600:.2f} hours")
            print(f"Downtime Last Day: {downtime_last_day / 3600:.2f} hours")
            print(f"Total Active Time (last week): {total_active_last_week.total_seconds() / 3600:.2f} hours")
            print(f"Downtime Last Week: {downtime_last_week / (7 * 24 * 3600):.2f} hours")
