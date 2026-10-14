import pytest
from fleet.serializers import AssignDriverSerializer,TripSerializer
from tests.factories import DriverFactory,VehicleFactory
pytestmark=pytest.mark.django_db
def payload(vehicle,driver): return {"vehicle":vehicle.pk,"driver":driver.pk,"start_location":"A","end_location":"B","start_time":"2030-01-01T10:00:00Z","distance_km":"12.5","route_points":[]}
def test_trip_accepts_active_vehicle(): assert TripSerializer(data=payload(VehicleFactory(status="active"),DriverFactory())).is_valid()
def test_trip_rejects_maintenance_vehicle():
    serializer=TripSerializer(data=payload(VehicleFactory(status="maintenance"),DriverFactory())); assert not serializer.is_valid(); assert "vehicle" in serializer.errors
def test_assign_driver_accepts_available_driver(): assert AssignDriverSerializer(data={"driver_id":DriverFactory(status="available").pk}).is_valid()
def test_assign_driver_rejects_unavailable_driver():
    serializer=AssignDriverSerializer(data={"driver_id":DriverFactory(status="on_trip").pk}); assert not serializer.is_valid(); assert "driver_id" in serializer.errors
