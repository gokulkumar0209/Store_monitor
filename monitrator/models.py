from django.db import models

class Store(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)  # Add any other store-related fields

    def __str__(self):
        return f"Store: {self.store_id}, Name: {self.name}"

class MenuHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"Store: {self.store.store_id}, Day: {self.day}"

class Timezone(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timezone_str = models.CharField(max_length=50)

    def __str__(self):
        return f"Store: {self.store.store_id}, Timezone: {self.timezone_str}"
    
class StoreStatus(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=10)  # Assuming 'active' or 'inactive'
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"Store: {self.store_id}, Status: {self.status}, Timestamp: {self.timestamp_utc}"    
