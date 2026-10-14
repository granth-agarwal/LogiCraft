import pytest
from accounts.serializers import ProfileSerializer
from tests.factories import ProfileFactory
pytestmark=pytest.mark.django_db
def test_role_cannot_be_changed_by_profile_patch():
    profile=ProfileFactory(role="customer"); result=ProfileSerializer(profile,data={"role":"admin","full_name":"New"},partial=True); assert result.is_valid(); saved=result.save(); assert saved.role=="customer"

