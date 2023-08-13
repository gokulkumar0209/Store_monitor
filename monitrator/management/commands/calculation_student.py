from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitrator.models import Store, MenuHours
import pandas as pd

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

            business_hours = MenuHours.objects.filter(store_id=store_id)

            for business_hour in business_hours:
                start_time_local = datetime.combine(datetime.today(), business_hour.start_time_local)
                end_time_local = datetime.combine(datetime.today(), business_hour.end_time_local)

                if start_time_local <= now <= end_time_local:
                    active = min(now, end_time_local) - max(start_time_local, last_hour)
                    total_active_time += active
                else:
                    downtime_last_hour += end_time_local - start_time_local

                if last_day < start_time_local <= now:
                    uptime_last_day = min(now, end_time_local) - start_time_local
                    total_active_last_day += uptime_last_day
                else:
                    downtime_last_day += end_time_local - start_time_local

                if last_week < start_time_local <= now:
                    uptime_last_week = min(now, end_time_local) - start_time_local
                    total_active_last_week += uptime_last_week

            data.append({
                'Store ID': store_id,
                'Total Active Time (last hour)': total_active_time.total_seconds() / 60,
                'Downtime Last Hour': downtime_last_hour.total_seconds() / 60,
                'Total Active Time (last day)': total_active_last_day.total_seconds() / 3600,
                'Downtime Last Day': downtime_last_day.total_seconds() / 3600,
                'Total Active Time (last week)': total_active_last_week.total_seconds() / 3600,
                'Downtime Last Week': downtime_last_week.total_seconds() / (7 * 24 * 3600)
            })

        df = pd.DataFrame(data)
        excel_path = 'Downloads/output.xlsx'  # Replace with your desired static path
        df.to_excel(excel_path, index=False)
        print(f"Data saved to Excel file: {excel_path}")
