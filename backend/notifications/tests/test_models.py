import pytest
from tests.factories import NotificationFactory
pytestmark=pytest.mark.django_db
def test_profile_delete_cascades_notifications():
    notification=NotificationFactory(); notification.recipient.delete(); from notifications.models import Notification; assert not Notification.objects.filter(pk=notification.pk).exists()

