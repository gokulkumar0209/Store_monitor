from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, StoreStatus, MenuHours

class Command(BaseCommand):
    help = 'Calculate uptime for stores'

    def handle(self, *args, **options):
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)

        all_stores = Store.objects.all()
        
        for store in all_stores:
            store_id = store.store_id
            active = timedelta(seconds=0)  # Initialize active time

            business_hours = MenuHours.objects.filter(store_id=store_id)
            
            for business_hour in business_hours:
                start_time_local = business_hour.start_time_local
                end_time_local = business_hour.end_time_local
                
                if start_time_local <= now <= end_time_local:
                    active += min(now, end_time_local) - max(start_time_local, last_hour)
            
            total_active_time = active.total_seconds()
            print(f"Store ID: {store_id}, Total Active Time (last hour): {total_active_time} seconds")
   
            if datetime.now > business_hour.start_time_local > last_day:
                    uptime_last_day = datetime.now - business_hour.start_time_local
                    if datetime.now > business_hour.end_time_local:
                        downtime_last_day = datetime.now-business_hour.end_time_local
                        active_last_day = uptime_last_day-downtime_last_day
                    else:
                        active_last_day = datetime.now-uptime_last_day
                total = total+active_last_day
            print(total)
            if datetime.now > business_hour.start_time_local > last_week:
                    uptime_last_week = datetime.now - business_hour.start_time_local
                    if datetime.now > business_hour.end_time_local:
                        downtime_last_week = datetime.now-business_hour.end_time_local
                        active_llast_week = uptime_last_week-downtime_last_week
                    else:
                        active_last_week = datetime.now-uptime_last_week
                total = total+active_last_week
            print(total)