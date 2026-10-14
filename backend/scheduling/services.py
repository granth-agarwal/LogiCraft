from decimal import Decimal
from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Booking, Schedule

@transaction.atomic
def book_schedule(*, schedule, customer):
    locked = Schedule.objects.select_for_update().select_related("route").get(pk=schedule.pk)
    active = set(locked.bookings.filter(status=Booking.Status.BOOKED).values_list("seat_number", flat=True))
    if len(active) >= locked.capacity: raise ValidationError({"capacity": "Schedule is fully booked."})
    seat = next(number for number in range(1, locked.capacity + 1) if number not in active)
    rate = Decimal(str(getattr(settings, "FLAT_RATE_PER_STOP", "10.00")))
    return Booking.objects.create(schedule=locked, customer=customer, seat_number=seat, fare=rate * max(len(locked.route.stops) - 1, 1))

