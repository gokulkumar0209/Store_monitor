from django.contrib import admin

# Register your models here.
from .models import MenuHours,Store,Timezone, StoreStatus

admin.site.register(MenuHours)
admin.site.register(Store)
admin.site.register(Timezone)
admin.site.register(StoreStatus)

