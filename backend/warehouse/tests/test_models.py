import pytest
from django.db import IntegrityError,transaction
from tests.factories import InventoryItemFactory
pytestmark=pytest.mark.django_db(transaction=True)
def test_negative_stock_rejected_by_database():
    with pytest.raises(IntegrityError):
        with transaction.atomic(): InventoryItemFactory(quantity=-1)
def test_sku_unique():
    item=InventoryItemFactory()
    with pytest.raises(IntegrityError):
        with transaction.atomic(): InventoryItemFactory(sku=item.sku)
def test_warehouse_delete_cascades_item():
    item=InventoryItemFactory(); item.warehouse.delete(); from warehouse.models import InventoryItem; assert not InventoryItem.objects.filter(pk=item.pk).exists()

