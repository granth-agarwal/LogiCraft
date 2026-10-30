import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("superuser,expected", [(True, 200), (False, 403)])
def test_local_login_csrf_roles_and_logout(settings, superuser, expected):
    settings.ENABLE_LOCAL_AUTH = True
    manager = get_user_model().objects
    create = manager.create_superuser if superuser else manager.create_user
    create(username="student", password="test-only-password")
    client = APIClient(enforce_csrf_checks=True)
    path = "/api/v1/auth/session/"
    assert client.get("/api/v1/profile/me/").status_code == 401
    assert client.get(path).status_code == 200
    assert client.post(path, {"username": "student", "password": "test-only-password"}, format="json").status_code == 403
    token = client.cookies["csrftoken"].value
    assert client.post(path, {"username": "student", "password": "wrong"}, format="json", HTTP_X_CSRFTOKEN=token).status_code == 401
    assert client.post(path, {"username": "student", "password": "test-only-password"}, format="json", HTTP_X_CSRFTOKEN=token).status_code == 200
    profile = client.get("/api/v1/profile/me/")
    assert profile.status_code == 200
    assert profile.data["role"] == ("admin" if superuser else "customer")
    assert client.get("/api/v1/fleet/vehicles/").status_code == expected
    assert client.delete(path, HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value).status_code == 200
    assert client.get("/api/v1/profile/me/").status_code == 401


def test_local_login_can_be_disabled(settings):
    settings.ENABLE_LOCAL_AUTH = False
    assert APIClient().get("/api/v1/auth/session/").status_code == 404
