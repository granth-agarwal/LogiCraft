import pytest
from django.db import IntegrityError
from tests.factories import ProfileFactory
pytestmark = pytest.mark.django_db
def test_supabase_user_id_is_unique():
    profile=ProfileFactory()
    with pytest.raises(IntegrityError): ProfileFactory(supabase_user_id=profile.supabase_user_id)

