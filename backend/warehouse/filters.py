import django_filters
from .models import InventoryItem
class InventoryItemFilter(django_filters.FilterSet):
    low_stock = django_filters.BooleanFilter(method="filter_low_stock")
    class Meta: model = InventoryItem; fields = ["warehouse", "category"]
    def filter_low_stock(self, qs, name, value):
        from django.db.models import F
        return qs.filter(quantity__lt=F("reorder_threshold")) if value else qs

