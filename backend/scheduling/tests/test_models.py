import pytest
from django.db import IntegrityError,transaction
from tests.factories import BookingFactory,ScheduleFactory
pytestmark=pytest.mark.django_db
def test_active_seat_is_unique_per_schedule():
    schedule=ScheduleFactory(); BookingFactory(schedule=schedule,seat_number=1)
    with pytest.raises(IntegrityError):
        with transaction.atomic(): BookingFactory(schedule=schedule,seat_number=1)
def test_schedule_delete_cascades_booking():
    booking=BookingFactory(); booking.schedule.delete(); from scheduling.models import Booking; assert not Booking.objects.filter(pk=booking.pk).exists()

