from django.db import transaction
from rest_framework.exceptions import ValidationError
from warehouse.services import adjust_inventory
from .models import Shipment, ShipmentEvent

TRANSITIONS = {
    Shipment.Status.PENDING: {Shipment.Status.PICKED_UP, Shipment.Status.FAILED},
    Shipment.Status.PICKED_UP: {Shipment.Status.IN_TRANSIT, Shipment.Status.FAILED},
    Shipment.Status.IN_TRANSIT: {Shipment.Status.DELIVERED, Shipment.Status.FAILED},
    Shipment.Status.DELIVERED: set(), Shipment.Status.FAILED: set(),
}

@transaction.atomic
def update_shipment_status(*, shipment, status, note, actor):
    locked = Shipment.objects.select_related("linked_item").select_for_update(of=("self",)).get(pk=shipment.pk)
    if status not in TRANSITIONS[locked.status]:
        raise ValidationError({"status": f"Cannot transition from {locked.status} to {status}."})
    if status == Shipment.Status.PICKED_UP and locked.linked_item:
        adjust_inventory(item=locked.linked_item, delta=-locked.quantity, reason=f"Shipment {locked.tracking_id} dispatch", actor=actor)
    locked.status = status; locked.save(update_fields=["status"])
    ShipmentEvent.objects.create(shipment=locked, status=status, note=note)
    return locked
