import django_filters
from .models import Shipment
class ShipmentFilter(django_filters.FilterSet):
    class Meta: model = Shipment; fields = ["status", "vehicle", "driver", "created_by"]

