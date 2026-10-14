import pytest
from accounts.models import Profile
from tests.factories import ProfileFactory
pytestmark=pytest.mark.django_db
def test_me_requires_authentication(api_client): assert api_client.get("/api/v1/profile/me/").status_code==401
def test_customer_cannot_list_users(auth,customer): assert auth(customer).get("/api/v1/users/").status_code==403
def test_admin_can_filter_users(auth,admin):
    response=auth(admin).get("/api/v1/users/?role=admin"); assert response.status_code==200; assert response.data["count"]>=1
@pytest.mark.parametrize("role,expected",[(Profile.Role.ADMIN,200),(Profile.Role.FLEET_MANAGER,403),(Profile.Role.WAREHOUSE_STAFF,403),(Profile.Role.CUSTOMER,403)])
def test_users_role_matrix(auth,role,expected): assert auth(ProfileFactory(role=role)).get("/api/v1/users/").status_code==expected
