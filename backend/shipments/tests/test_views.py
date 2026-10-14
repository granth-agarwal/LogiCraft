import pytest
from accounts.models import Profile
from tests.factories import ProfileFactory,ShipmentFactory
pytestmark=pytest.mark.django_db
def test_shipments_require_auth(api_client): assert api_client.get("/api/v1/shipments/").status_code==401
def test_customer_only_sees_owned(auth,customer):
    own=ShipmentFactory(created_by=customer); ShipmentFactory(); response=auth(customer).get("/api/v1/shipments/"); assert [x["id"] for x in response.data["results"]]==[own.pk]
def test_customer_cannot_update_status(auth,customer):
    shipment=ShipmentFactory(created_by=customer); assert auth(customer).post(f"/api/v1/shipments/{shipment.pk}/update-status/",{"status":"picked_up"}).status_code==403
@pytest.mark.parametrize("role",[Profile.Role.ADMIN,Profile.Role.FLEET_MANAGER,Profile.Role.WAREHOUSE_STAFF,Profile.Role.CUSTOMER])
def test_shipments_list_role_matrix(auth,role): assert auth(ProfileFactory(role=role)).get("/api/v1/shipments/").status_code==200
@pytest.mark.parametrize("role",[Profile.Role.ADMIN,Profile.Role.FLEET_MANAGER,Profile.Role.WAREHOUSE_STAFF])
def test_operations_roles_can_advance_shipments(auth,role):
    actor=ProfileFactory(role=role); shipment=ShipmentFactory(); assert auth(actor).post(f"/api/v1/shipments/{shipment.pk}/update-status/",{"status":"picked_up"}).status_code==200
