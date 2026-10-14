from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from common.permissions import IsOwnerOrAdmin
from common.viewsets import OperationsModelViewSet
from .models import Booking, Route, Schedule
from .serializers import BookingSerializer, RouteSerializer, ScheduleSerializer
from .services import book_schedule
from .permissions import CanManageScheduling

class RouteViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageScheduling]
    queryset = Route.objects.order_by("id"); serializer_class = RouteSerializer; search_fields = ["name"]
class ScheduleViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageScheduling]
    queryset = Schedule.objects.select_related("route", "vehicle").order_by("id"); serializer_class = ScheduleSerializer
    filterset_fields = ["route", "vehicle"]; ordering_fields = ["departure_time", "capacity"]
    def get_permissions(self):
        if self.action in ("list", "retrieve", "book"): return [IsAuthenticated()]
        return super().get_permissions()
    @action(detail=True, methods=["post"])
    def book(self, request, pk=None):
        booking = book_schedule(schedule=self.get_object(), customer=request.user)
        return Response(BookingSerializer(booking).data, status=201)

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    def get_queryset(self):
        qs = Booking.objects.select_related("schedule", "customer").order_by("id")
        return qs if self.request.user.role != "customer" else qs.filter(customer=self.request.user)
    def get_permissions(self):
        if self.action == "cancel": return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action in ("list", "retrieve"): return [IsAuthenticated()]
        return [IsAuthenticated(), CanManageScheduling()]
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status != Booking.Status.BOOKED: return Response({"detail": "Only booked reservations can be cancelled."}, status=400)
        booking.status = Booking.Status.CANCELLED; booking.save(update_fields=["status"])
        return Response(self.get_serializer(booking).data)
