from datetime import timedelta, datetime
from django.db.models import Q
from monitrator.models import Store, MenuHours, StoreStatus, Timezone
from pytz import timezone

def generate_report():
    stores = Store.objects.all()

    report = []

    for store in stores:
        business_hours = MenuHours.objects.filter(store=store)
        timezone = Timezone.objects.get(store=store).timezone_str

        now_utc = datetime.utcnow()
        now_local = now_utc.strftime('%Y-%m-%d %H:%M:%S')

        total_uptime_hour = timedelta()
        total_downtime_hour = timedelta()

        for day in range(7):  # 0=Monday, 6=Sunday
            day_hours = business_hours.filter(day=day).first()

            if day_hours:
                start_time_local = day_hours.start_time_local
                end_time_local = day_hours.end_time_local

                start_time_utc = convert_to_utc(now_local, start_time_local, timezone)
                end_time_utc = convert_to_utc(now_local, end_time_local, timezone)

                store_status_entries = StoreStatus.objects.filter(
                    Q(store_id=store.store_id),
                    Q(timestamp_utc__gte=start_time_utc),
                    Q(timestamp_utc__lt=end_time_utc)
                ).order_by('timestamp_utc')

                current_status = 'inactive'
                current_period_start = start_time_utc

                for status_entry in store_status_entries:
                    timestamp = status_entry.timestamp_utc
                    status = status_entry.status

                    if current_status != status:
                        if current_status == 'active':
                            total_uptime_hour += timestamp - current_period_start
                        else:
                            total_downtime_hour += timestamp - current_period_start

                        current_status = status
                        current_period_start = timestamp

                # Handle the last period
                if current_status == 'active':
                    total_uptime_hour += end_time_utc - current_period_start
                else:
                    total_downtime_hour += end_time_utc - current_period_start

        report_entry = {
            'store_id': store.store_id,
            'uptime_last_hour': total_uptime_hour.total_seconds() / 60,
            'downtime_last_hour': total_downtime_hour.total_seconds() / 60,
            # Calculate uptime and downtime for the last day and last week similarly
            # ...
        }

        report.append(report_entry)

    return report

def convert_to_utc(local_datetime, local_time, timezone_str):
    local_tz = timezone(timezone_str)
    local_datetime = local_datetime.replace(hour=local_time.hour, minute=local_time.minute, second=local_time.second)
    
    local_dt_with_tz = local_tz.localize(local_datetime)
    utc_dt = local_dt_with_tz.astimezone(timezone('UTC'))
    
    return utc_dt
# def convert_to_utc(local_datetime, local_time, timezone):
#     # Convert a local time to UTC time
#     # You will need to implement the conversion based on the provided timezone
#     # ...
#     return utc_time
