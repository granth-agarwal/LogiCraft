from datetime import timedelta
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from fleet.models import Vehicle
from shipments.models import Shipment
from warehouse.models import InventoryItem
from scheduling.models import Booking

class SummaryView(APIView):
    def get(self, request):
        today = timezone.localdate()
        return Response({"active_vehicles": Vehicle.objects.filter(status=Vehicle.Status.ACTIVE).count(), "pending_shipments": Shipment.objects.filter(status=Shipment.Status.PENDING).count(), "low_stock_items": InventoryItem.objects.filter(quantity__lt=F("reorder_threshold")).count(), "todays_bookings": Booking.objects.filter(created_at__date=today).count()})

class ShipmentsByStatusView(APIView):
    def get(self, request): return Response(list(Shipment.objects.values("status").annotate(count=Count("id")).order_by("status")))

class RevenueView(APIView):
    def get(self, request):
        start = timezone.localdate() - timedelta(days=29)
        rows = Booking.objects.filter(created_at__date__gte=start).annotate(day=TruncDate("created_at")).values("day").annotate(revenue=Sum("fare")).order_by("day")
        return Response(list(rows))
