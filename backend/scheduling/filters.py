import django_filters
from .models import Schedule
class ScheduleFilter(django_filters.FilterSet):
    departure_after = django_filters.IsoDateTimeFilter(field_name="departure_time", lookup_expr="gte")
    class Meta: model = Schedule; fields = ["route", "vehicle"]

