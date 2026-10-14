import pytest
from tests.factories import InventoryItemFactory,ShipmentFactory
from shipments.models import ShipmentEvent
from warehouse.models import StockMovement
pytestmark=pytest.mark.django_db
def test_dispatch_deducts_stock_and_creates_event(auth,admin):
    item=InventoryItemFactory(quantity=5); shipment=ShipmentFactory(linked_item=item,quantity=3,status="pending"); response=auth(admin).post(f"/api/v1/shipments/{shipment.pk}/update-status/",{"status":"picked_up","note":"Loaded"}); assert response.status_code==200; item.refresh_from_db(); assert item.quantity==2; assert StockMovement.objects.filter(item=item,quantity=3).exists(); assert ShipmentEvent.objects.filter(shipment=shipment,status="picked_up").exists()
def test_dispatch_insufficient_inventory_rolls_everything_back(auth,admin):
    item=InventoryItemFactory(quantity=1); shipment=ShipmentFactory(linked_item=item,quantity=2,status="pending"); response=auth(admin).post(f"/api/v1/shipments/{shipment.pk}/update-status/",{"status":"picked_up"}); assert response.status_code==400; item.refresh_from_db(); shipment.refresh_from_db(); assert item.quantity==1; assert shipment.status=="pending"; assert not ShipmentEvent.objects.filter(shipment=shipment).exists(); assert not StockMovement.objects.filter(item=item).exists()

