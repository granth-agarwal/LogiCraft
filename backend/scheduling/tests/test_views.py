import pytest
from accounts.models import Profile
from tests.factories import BookingFactory,ProfileFactory,ScheduleFactory
pytestmark=pytest.mark.django_db
def test_scheduling_requires_auth(api_client): assert api_client.get("/api/v1/scheduling/schedules/").status_code==401
def test_customer_cannot_create_route(auth,customer): assert auth(customer).post("/api/v1/scheduling/routes/",{"name":"A","stops":["A","B"],"estimated_duration_minutes":10},format="json").status_code==403
def test_authenticated_customer_can_list_schedules(auth,customer): ScheduleFactory(); assert auth(customer).get("/api/v1/scheduling/schedules/").status_code==200
def test_admin_can_create_booking(auth,admin,customer):
    schedule=ScheduleFactory(); response=auth(admin).post("/api/v1/scheduling/bookings/",{"schedule":schedule.pk,"customer":customer.pk,"seat_number":1,"status":"booked","fare":"25.00"}); assert response.status_code==201
def test_customer_sees_only_own_bookings(auth,customer):
    own=BookingFactory(customer=customer); BookingFactory(); response=auth(customer).get("/api/v1/scheduling/bookings/"); assert [x["id"] for x in response.data["results"]]==[own.pk]
def test_customer_can_cancel_own_booking(auth,customer):
    booking=BookingFactory(customer=customer); response=auth(customer).post(f"/api/v1/scheduling/bookings/{booking.pk}/cancel/"); assert response.status_code==200; assert response.data["status"]=="cancelled"
def test_cancel_rejects_non_booked(auth,admin):
    booking=BookingFactory(status="completed"); assert auth(admin).post(f"/api/v1/scheduling/bookings/{booking.pk}/cancel/").status_code==400
@pytest.mark.parametrize("role",[Profile.Role.ADMIN,Profile.Role.FLEET_MANAGER,Profile.Role.WAREHOUSE_STAFF,Profile.Role.CUSTOMER])
@pytest.mark.parametrize("url",["/api/v1/scheduling/schedules/","/api/v1/scheduling/bookings/"])
def test_customer_scoped_scheduling_lists_allow_all_roles(auth,role,url): assert auth(ProfileFactory(role=role)).get(url).status_code==200
@pytest.mark.parametrize("role,expected",[(Profile.Role.ADMIN,200),(Profile.Role.FLEET_MANAGER,200),(Profile.Role.WAREHOUSE_STAFF,403),(Profile.Role.CUSTOMER,403)])
def test_route_role_matrix(auth,role,expected): assert auth(ProfileFactory(role=role)).get("/api/v1/scheduling/routes/").status_code==expected
