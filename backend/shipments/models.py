import uuid
from django.db import models

def tracking_id(): return f"LC-{uuid.uuid4().hex[:12].upper()}"

class Shipment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PICKED_UP = "picked_up", "Picked up"
        IN_TRANSIT = "in_transit", "In transit"
        DELIVERED = "delivered", "Delivered"
        FAILED = "failed", "Failed"
    tracking_id = models.CharField(max_length=32, unique=True, default=tracking_id, editable=False)
    origin = models.CharField(max_length=255); destination = models.CharField(max_length=255)
    vehicle = models.ForeignKey("fleet.Vehicle", null=True, blank=True, on_delete=models.SET_NULL, related_name="shipments")
    driver = models.ForeignKey("fleet.Driver", null=True, blank=True, on_delete=models.SET_NULL, related_name="shipments")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    linked_item = models.ForeignKey("warehouse.InventoryItem", null=True, blank=True, on_delete=models.SET_NULL, related_name="shipments")
    quantity = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT, related_name="shipments")
    created_at = models.DateTimeField(auto_now_add=True)

class ShipmentEvent(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="events")
    status = models.CharField(max_length=16, choices=Shipment.Status.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    class Meta: ordering = ["timestamp", "id"]

