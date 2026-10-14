from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import Profile
from scheduling.models import Booking
from shipments.models import ShipmentEvent
from warehouse.models import InventoryItem
from .models import Notification

@receiver(pre_save, sender=InventoryItem)
def remember_previous_quantity(sender, instance, **kwargs):
    instance._was_low = False if not instance.pk else sender.objects.filter(pk=instance.pk, quantity__lt=F("reorder_threshold")).exists()

@receiver(post_save, sender=InventoryItem)
def notify_low_stock(sender, instance, **kwargs):
    if instance.quantity < instance.reorder_threshold and not getattr(instance, "_was_low", False):
        recipients = Profile.objects.filter(warehouse=instance.warehouse, role__in=[Profile.Role.ADMIN, Profile.Role.WAREHOUSE_STAFF])
        Notification.objects.bulk_create([Notification(recipient=p, type=Notification.Type.LOW_STOCK, message=f"{instance.name} ({instance.sku}) is below its reorder threshold.") for p in recipients])

@receiver(post_save, sender=ShipmentEvent)
def notify_shipment_event(sender, instance, created, **kwargs):
    if created: Notification.objects.create(recipient=instance.shipment.created_by, type=Notification.Type.SHIPMENT_UPDATE, message=f"Shipment {instance.shipment.tracking_id} is now {instance.get_status_display()}.")

@receiver(post_save, sender=Booking)
def notify_booking(sender, instance, created, **kwargs):
    if created: Notification.objects.create(recipient=instance.customer, type=Notification.Type.BOOKING_CONFIRMED, message=f"Booking confirmed for seat {instance.seat_number} on {instance.schedule.route.name}.")

