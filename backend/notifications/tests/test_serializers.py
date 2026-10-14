import pytest
from notifications.serializers import NotificationSerializer
from tests.factories import NotificationFactory
pytestmark=pytest.mark.django_db
def test_notification_fields_are_read_only():
    n=NotificationFactory(); s=NotificationSerializer(n,data={"message":"Tampered","is_read":True},partial=True); assert s.is_valid(); saved=s.save(); assert saved.message=="Update" and not saved.is_read

