import pytest
from accounts.models import Profile
from tests.factories import InventoryItemFactory,ProfileFactory
pytestmark=pytest.mark.django_db
def test_warehouse_requires_auth(api_client): assert api_client.get("/api/v1/warehouse/items/").status_code==401
def test_customer_forbidden(auth,customer): assert auth(customer).get("/api/v1/warehouse/items/").status_code==403
@pytest.mark.parametrize("role,expected",[(Profile.Role.ADMIN,200),(Profile.Role.FLEET_MANAGER,403),(Profile.Role.WAREHOUSE_STAFF,200),(Profile.Role.CUSTOMER,403)])
@pytest.mark.parametrize("url",["/api/v1/warehouse/warehouses/","/api/v1/warehouse/items/","/api/v1/warehouse/movements/"])
def test_warehouse_role_matrix(auth,role,expected,url): assert auth(ProfileFactory(role=role)).get(url).status_code==expected
def test_low_stock_endpoint(auth,admin):
    low=InventoryItemFactory(quantity=1,reorder_threshold=2); InventoryItemFactory(quantity=3,reorder_threshold=2); response=auth(admin).get("/api/v1/warehouse/items/low-stock/"); assert response.status_code==200; assert [x["id"] for x in response.data]==[low.pk]
