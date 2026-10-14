from django.contrib import admin
from .models import Driver, MaintenanceRecord, Trip, Vehicle
admin.site.register([Driver, Vehicle, Trip, MaintenanceRecord])

