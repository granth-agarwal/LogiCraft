from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from common.permissions import IsOwnerOrAdmin
from .models import Notification
from .serializers import NotificationSerializer
class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    filterset_fields = ["is_read", "type"]
    def get_queryset(self): return Notification.objects.filter(recipient=self.request.user)
    @action(detail=True, methods=["post"], url_path="mark-read", permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def mark_read(self, request, pk=None):
        notification = self.get_object(); notification.is_read = True; notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)

