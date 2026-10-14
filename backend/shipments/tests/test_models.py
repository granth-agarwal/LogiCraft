import pytest
from django.db import IntegrityError,transaction
from tests.factories import ShipmentFactory
pytestmark=pytest.mark.django_db
def test_tracking_id_is_generated_and_unique():
    one,two=ShipmentFactory(),ShipmentFactory(); assert one.tracking_id.startswith("LC-"); assert one.tracking_id!=two.tracking_id
def test_tracking_id_constraint():
    one=ShipmentFactory()
    with pytest.raises(IntegrityError):
        with transaction.atomic(): ShipmentFactory(tracking_id=one.tracking_id)
def test_shipment_delete_cascades_events():
    from tests.factories import ShipmentEventFactory
    event=ShipmentEventFactory(); event.shipment.delete(); from shipments.models import ShipmentEvent; assert not ShipmentEvent.objects.filter(pk=event.pk).exists()

