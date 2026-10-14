import pytest
from tests.factories import BookingFactory,ScheduleFactory
pytestmark=pytest.mark.django_db
def test_booking_exact_capacity_boundary_succeeds(auth,customer):
    schedule=ScheduleFactory(capacity=2); BookingFactory(schedule=schedule,seat_number=1); response=auth(customer).post(f"/api/v1/scheduling/schedules/{schedule.pk}/book/"); assert response.status_code==201; assert response.data["seat_number"]==2
def test_booking_over_capacity_rejected(auth,customer):
    schedule=ScheduleFactory(capacity=1); BookingFactory(schedule=schedule,seat_number=1); response=auth(customer).post(f"/api/v1/scheduling/schedules/{schedule.pk}/book/"); assert response.status_code==400; assert schedule.bookings.count()==1

