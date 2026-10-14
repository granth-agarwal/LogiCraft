import pytest
from rest_framework.test import APIClient
from tests.factories import ProfileFactory
from accounts.models import Profile

@pytest.fixture
def api_client(): return APIClient()
@pytest.fixture
def admin(): return ProfileFactory(role=Profile.Role.ADMIN)
@pytest.fixture
def fleet_manager(): return ProfileFactory(role=Profile.Role.FLEET_MANAGER)
@pytest.fixture
def warehouse_staff(): return ProfileFactory(role=Profile.Role.WAREHOUSE_STAFF)
@pytest.fixture
def customer(): return ProfileFactory(role=Profile.Role.CUSTOMER)
@pytest.fixture
def auth(api_client):
    def login(user): api_client.force_authenticate(user=user); return api_client
    return login

