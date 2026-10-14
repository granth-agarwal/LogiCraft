import pytest
from tests.factories import InventoryItemFactory
from warehouse.models import StockMovement
pytestmark=pytest.mark.django_db
def test_adjust_stock_updates_item_and_writes_movement(auth,admin):
    item=InventoryItemFactory(quantity=5); response=auth(admin).post(f"/api/v1/warehouse/items/{item.pk}/adjust-stock/",{"delta":-3,"reason":"Pick"}); assert response.status_code==200; item.refresh_from_db(); assert item.quantity==2; assert StockMovement.objects.get(item=item).quantity==3
def test_adjust_stock_rolls_back_when_insufficient(auth,admin):
    item=InventoryItemFactory(quantity=2); response=auth(admin).post(f"/api/v1/warehouse/items/{item.pk}/adjust-stock/",{"delta":-3,"reason":"Pick"}); assert response.status_code==400; item.refresh_from_db(); assert item.quantity==2; assert not StockMovement.objects.filter(item=item).exists()

