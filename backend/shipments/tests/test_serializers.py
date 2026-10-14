import pytest
from shipments.serializers import StatusUpdateSerializer
from tests.factories import ShipmentFactory
pytestmark=pytest.mark.django_db
def test_legal_transition_valid(): assert StatusUpdateSerializer(data={"status":"picked_up"},context={"shipment":ShipmentFactory(status="pending")}).is_valid()
def test_pending_to_delivered_rejected():
    s=StatusUpdateSerializer(data={"status":"delivered"},context={"shipment":ShipmentFactory(status="pending")}); assert not s.is_valid(); assert "status" in s.errors

