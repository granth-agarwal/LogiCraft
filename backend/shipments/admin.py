from django.contrib import admin
from .models import Shipment, ShipmentEvent
admin.site.register([Shipment, ShipmentEvent])

