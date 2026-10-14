import pytest
from tests.factories import DriverFactory,TripFactory,VehicleFactory
pytestmark=pytest.mark.django_db
def test_assign_driver_action(auth,admin):
    vehicle=VehicleFactory(current_driver=None); driver=DriverFactory(); response=auth(admin).post(f"/api/v1/fleet/vehicles/{vehicle.pk}/assign-driver/",{"driver_id":driver.pk}); assert response.status_code==200; vehicle.refresh_from_db(); assert vehicle.current_driver==driver
def test_vehicle_trips_action(auth,admin):
    trip=TripFactory(); response=auth(admin).get(f"/api/v1/fleet/vehicles/{trip.vehicle_id}/trips/"); assert response.status_code==200; assert response.data[0]["id"]==trip.pk
