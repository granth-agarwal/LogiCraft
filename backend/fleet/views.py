from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.viewsets import OperationsModelViewSet
from .models import Driver, MaintenanceRecord, Trip, Vehicle
from .serializers import AssignDriverSerializer, DriverSerializer, MaintenanceRecordSerializer, TripSerializer, VehicleSerializer
from .permissions import CanManageFleet

class VehicleViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageFleet]
    queryset = Vehicle.objects.select_related("current_driver").order_by("id")
    serializer_class = VehicleSerializer
    filterset_fields = ["type", "status", "current_driver"]
    search_fields = ["registration_number"]
    ordering_fields = ["registration_number", "capacity_kg", "status"]
    @action(detail=True, methods=["post"], url_path="assign-driver")
    def assign_driver(self, request, pk=None):
        serializer = AssignDriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = self.get_object()
        vehicle.current_driver = serializer.validated_data["driver"]
        vehicle.save(update_fields=["current_driver"])
        return Response(self.get_serializer(vehicle).data)
    @action(detail=True, methods=["get"])
    def trips(self, request, pk=None):
        return Response(TripSerializer(self.get_object().trips.all(), many=True).data)

class DriverViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageFleet]
    queryset = Driver.objects.select_related("profile").order_by("id"); serializer_class = DriverSerializer
    filterset_fields = ["status"]; search_fields = ["license_number", "profile__full_name"]

class TripViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageFleet]
    queryset = Trip.objects.select_related("vehicle", "driver").order_by("id"); serializer_class = TripSerializer
    filterset_fields = ["status", "vehicle", "driver"]; search_fields = ["start_location", "end_location"]

class MaintenanceRecordViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageFleet]
    queryset = MaintenanceRecord.objects.select_related("vehicle").order_by("id"); serializer_class = MaintenanceRecordSerializer
    filterset_fields = ["vehicle"]; ordering_fields = ["service_date", "next_due_date", "cost"]
