import pytest
from warehouse.serializers import InventoryItemSerializer
from tests.factories import WarehouseFactory
pytestmark=pytest.mark.django_db
def test_negative_stock_rejected_by_serializer():
    s=InventoryItemSerializer(data={"sku":"X","name":"X","category":"X","quantity":-1,"reorder_threshold":0,"warehouse":WarehouseFactory().pk}); assert not s.is_valid(); assert "quantity" in s.errors
def test_nonnegative_stock_is_valid():
    s=InventoryItemSerializer(data={"sku":"X","name":"X","category":"X","quantity":0,"reorder_threshold":0,"warehouse":WarehouseFactory().pk}); assert s.is_valid(),s.errors

