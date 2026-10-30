from django.db import models
from django.db.models import Case, F, Value, When

class Route(models.Model):
    name = models.CharField(max_length=255)
    stops = models.JSONField(default=list)
    estimated_duration_minutes = models.PositiveIntegerField()
    def __str__(self): return self.name

class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    departure_time = models.DateTimeField()
    vehicle = models.ForeignKey("fleet.Vehicle", on_delete=models.PROTECT, related_name="schedules")
    capacity = models.PositiveIntegerField()

class Booking(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked", "Booked"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT, related_name="bookings")
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.BOOKED)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    active_seat = models.GeneratedField(
        expression=Case(When(status="booked", then=F("seat_number")), default=Value(None)),
        output_field=models.PositiveIntegerField(null=True), db_persist=True,
    )
    class Meta:
        constraints = [models.UniqueConstraint(fields=["schedule", "active_seat"], name="unique_active_schedule_seat")]

