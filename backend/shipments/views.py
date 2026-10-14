from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.permissions import IsOperations, IsOwnerOrAdmin
from .models import Shipment
from .serializers import ShipmentSerializer, StatusUpdateSerializer
from .services import update_shipment_status
from rest_framework.viewsets import ModelViewSet

class ShipmentViewSet(ModelViewSet):
    serializer_class = ShipmentSerializer
    filterset_fields = ["status", "vehicle", "driver"]; search_fields = ["tracking_id", "origin", "destination"]; ordering_fields = ["created_at", "status"]
    def get_queryset(self):
        qs = Shipment.objects.select_related("vehicle", "driver", "linked_item", "created_by").prefetch_related("events").order_by("id")
        return qs if self.request.user.role != "customer" else qs.filter(created_by=self.request.user)
    def get_permissions(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy"): return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action == "update_status": return [IsAuthenticated(), IsOperations()]
        return [IsAuthenticated()]
    def perform_create(self, serializer): serializer.save(created_by=self.request.user)
    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        shipment = self.get_object(); serializer = StatusUpdateSerializer(data=request.data, context={"shipment": shipment}); serializer.is_valid(raise_exception=True)
        result = update_shipment_status(shipment=shipment, status=serializer.validated_data["status"], note=serializer.validated_data.get("note", ""), actor=request.user)
        return Response(self.get_serializer(result).data)
