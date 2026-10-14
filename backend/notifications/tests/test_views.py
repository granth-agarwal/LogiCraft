import pytest
from accounts.models import Profile
from tests.factories import NotificationFactory,ProfileFactory
pytestmark=pytest.mark.django_db
def test_notifications_require_auth(api_client): assert api_client.get("/api/v1/notifications/").status_code==401
def test_recipient_can_mark_read(auth,customer):
    n=NotificationFactory(recipient=customer); response=auth(customer).post(f"/api/v1/notifications/{n.pk}/mark-read/"); assert response.status_code==200; n.refresh_from_db(); assert n.is_read
def test_user_cannot_see_another_users_notification(auth,customer):
    NotificationFactory(); assert auth(customer).get("/api/v1/notifications/").data["count"]==0
@pytest.mark.parametrize("role",[Profile.Role.ADMIN,Profile.Role.FLEET_MANAGER,Profile.Role.WAREHOUSE_STAFF,Profile.Role.CUSTOMER])
def test_notification_role_matrix(auth,role):
    profile=ProfileFactory(role=role); NotificationFactory(recipient=profile); assert auth(profile).get("/api/v1/notifications/").data["count"]==1
