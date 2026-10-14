import uuid
from types import SimpleNamespace
from unittest.mock import Mock,patch
import pytest
from rest_framework.test import APIRequestFactory
from accounts.authentication import SupabaseJWTAuthentication
pytestmark=pytest.mark.django_db
def test_supabase_jwks_and_claims_create_shadow_profile():
    request=APIRequestFactory().get("/",HTTP_AUTHORIZATION="Bearer jwt")
    client=Mock(); client.get_signing_key_from_jwt.return_value=SimpleNamespace(key="key")
    claims={"sub":str(uuid.uuid4()),"email":"ops@example.com","app_metadata":{"role":"fleet_manager"}}
    with patch("accounts.authentication._jwks_client",return_value=client),patch("accounts.authentication.jwt.decode",return_value=claims):
        profile,_=SupabaseJWTAuthentication().authenticate(request)
    assert profile.role=="fleet_manager"; client.get_signing_key_from_jwt.assert_called_once_with("jwt")

