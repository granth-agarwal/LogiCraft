from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import InventoryItem, StockMovement

@transaction.atomic
def adjust_inventory(*, item, delta, reason, actor):
    locked = InventoryItem.objects.select_for_update().get(pk=item.pk)
    new_quantity = locked.quantity + delta
    if new_quantity < 0:
        raise ValidationError({"quantity": "Stock quantity cannot be negative."})
    locked.quantity = new_quantity
    locked.save(update_fields=["quantity"])
    StockMovement.objects.create(item=locked, warehouse=locked.warehouse,
        movement_type=StockMovement.Type.INBOUND if delta > 0 else StockMovement.Type.OUTBOUND,
        quantity=abs(delta), reason=reason, created_by=actor)
    return locked

