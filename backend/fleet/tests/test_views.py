import pytest
from accounts.models import Profile
from tests.factories import ProfileFactory,VehicleFactory
pytestmark=pytest.mark.django_db
@pytest.mark.parametrize("url",["/api/v1/fleet/vehicles/","/api/v1/fleet/drivers/","/api/v1/fleet/trips/","/api/v1/fleet/maintenance/"])
def test_fleet_endpoints_require_auth(api_client,url): assert api_client.get(url).status_code==401
def test_customer_cannot_manage_fleet(auth,customer): assert auth(customer).get("/api/v1/fleet/vehicles/").status_code==403
@pytest.mark.parametrize("role,expected",[(Profile.Role.ADMIN,200),(Profile.Role.FLEET_MANAGER,200),(Profile.Role.WAREHOUSE_STAFF,403),(Profile.Role.CUSTOMER,403)])
@pytest.mark.parametrize("url",["/api/v1/fleet/vehicles/","/api/v1/fleet/drivers/","/api/v1/fleet/trips/","/api/v1/fleet/maintenance/"])
def test_fleet_role_matrix(auth,role,expected,url): assert auth(ProfileFactory(role=role)).get(url).status_code==expected
def test_admin_vehicle_crud(auth,admin):
    client=auth(admin); response=client.post("/api/v1/fleet/vehicles/",{"registration_number":"OPS-1","type":"truck","capacity_kg":"1000","status":"active"}); assert response.status_code==201; assert client.delete(f"/api/v1/fleet/vehicles/{response.data['id']}/").status_code==204
