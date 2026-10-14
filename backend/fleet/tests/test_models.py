import pytest
from django.db import IntegrityError
from tests.factories import DriverFactory,TripFactory,VehicleFactory
pytestmark=pytest.mark.django_db
def test_vehicle_registration_unique():
    vehicle=VehicleFactory()
    with pytest.raises(IntegrityError): VehicleFactory(registration_number=vehicle.registration_number)
def test_vehicle_delete_cascades_trips():
    trip=TripFactory(); trip.vehicle.delete(); from fleet.models import Trip; assert not Trip.objects.filter(pk=trip.pk).exists()

