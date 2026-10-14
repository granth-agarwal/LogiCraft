import pytest
from tests.factories import BookingFactory,InventoryItemFactory,ProfileFactory,ShipmentEventFactory,ShipmentFactory,WarehouseFactory
from notifications.models import Notification
pytestmark=pytest.mark.django_db
def test_shipment_event_notifies_customer():
    shipment=ShipmentFactory(); ShipmentEventFactory(shipment=shipment); assert Notification.objects.filter(recipient=shipment.created_by,type="shipment_update").exists()
def test_booking_notifies_customer():
    booking=BookingFactory(); assert Notification.objects.filter(recipient=booking.customer,type="booking_confirmed").exists()
def test_low_stock_crossing_notifies_warehouse_staff():
    manager=ProfileFactory(role="warehouse_staff"); warehouse=WarehouseFactory(manager=manager); manager.warehouse=warehouse; manager.save(); item=InventoryItemFactory(warehouse=warehouse,quantity=5,reorder_threshold=3); item.quantity=2; item.save(); assert Notification.objects.filter(recipient=manager,type="low_stock").exists()

