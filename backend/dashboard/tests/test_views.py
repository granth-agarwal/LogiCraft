import pytest
from accounts.models import Profile
from tests.factories import ProfileFactory
pytestmark=pytest.mark.django_db
@pytest.mark.parametrize("url",["/api/v1/dashboard/summary/","/api/v1/dashboard/shipments-by-status/","/api/v1/dashboard/revenue/"])
def test_dashboard_requires_auth(api_client,url): assert api_client.get(url).status_code==401
def test_summary_shape(auth,admin):
    response=auth(admin).get("/api/v1/dashboard/summary/"); assert response.status_code==200; assert set(response.data)=={"active_vehicles","pending_shipments","low_stock_items","todays_bookings"}
def test_chart_endpoints_return_series(auth,admin):
    from tests.factories import BookingFactory,ShipmentFactory
    BookingFactory(fare=42); ShipmentFactory(status="pending"); assert auth(admin).get("/api/v1/dashboard/revenue/").data[0]["revenue"]==42; assert auth(admin).get("/api/v1/dashboard/shipments-by-status/").data[0]["count"]==1
@pytest.mark.parametrize("role",[Profile.Role.ADMIN,Profile.Role.FLEET_MANAGER,Profile.Role.WAREHOUSE_STAFF,Profile.Role.CUSTOMER])
@pytest.mark.parametrize("url",["/api/v1/dashboard/summary/","/api/v1/dashboard/shipments-by-status/","/api/v1/dashboard/revenue/"])
def test_dashboard_role_matrix(auth,role,url): assert auth(ProfileFactory(role=role)).get(url).status_code==200
