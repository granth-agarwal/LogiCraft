from django.contrib import admin
from .models import InventoryItem, StockMovement, Warehouse
admin.site.register([Warehouse, InventoryItem, StockMovement])

