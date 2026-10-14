from django.db import models
class Notification(models.Model):
    class Type(models.TextChoices):
        SHIPMENT_UPDATE = "shipment_update", "Shipment update"
        LOW_STOCK = "low_stock", "Low stock"
        BOOKING_CONFIRMED = "booking_confirmed", "Booking confirmed"
    recipient = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=500)
    type = models.CharField(max_length=24, choices=Type.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]

