import django_filters
from .models import Trip
class TripFilter(django_filters.FilterSet):
    start_after = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_before = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="lte")
    class Meta: model = Trip; fields = ["status", "vehicle", "driver"]

