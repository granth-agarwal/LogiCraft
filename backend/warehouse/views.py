from django.db.models import F
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.viewsets import OperationsModelViewSet
from .models import InventoryItem, StockMovement, Warehouse
from .serializers import InventoryItemSerializer, StockAdjustmentSerializer, StockMovementSerializer, WarehouseSerializer
from .services import adjust_inventory
from .permissions import CanManageWarehouse

class WarehouseViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageWarehouse]
    queryset = Warehouse.objects.select_related("manager").order_by("id"); serializer_class = WarehouseSerializer
    search_fields = ["name", "address"]
class InventoryItemViewSet(OperationsModelViewSet):
    permission_classes = [IsAuthenticated, CanManageWarehouse]
    queryset = InventoryItem.objects.select_related("warehouse").order_by("id"); serializer_class = InventoryItemSerializer
    filterset_fields = ["category", "warehouse"]; search_fields = ["sku", "name", "category"]; ordering_fields = ["sku", "name", "quantity"]
    @action(detail=False, methods=["get"], url_path="low-stock")
    def low_stock(self, request):
        rows = self.filter_queryset(self.get_queryset().filter(quantity__lt=F("reorder_threshold")))
        return Response(self.get_serializer(rows, many=True).data)
    @action(detail=True, methods=["post"], url_path="adjust-stock")
    def adjust_stock(self, request, pk=None):
        serializer = StockAdjustmentSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        item = adjust_inventory(item=self.get_object(), delta=serializer.validated_data["delta"], reason=serializer.validated_data["reason"], actor=request.user)
        return Response(self.get_serializer(item).data)
class StockMovementViewSet(OperationsModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    permission_classes = [IsAuthenticated, CanManageWarehouse]
    queryset = StockMovement.objects.select_related("item", "warehouse", "created_by").order_by("id"); serializer_class = StockMovementSerializer
    filterset_fields = ["item", "warehouse", "movement_type"]; ordering_fields = ["created_at"]
    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data
        delta = data["quantity"] if data["movement_type"] == StockMovement.Type.INBOUND else -data["quantity"]
        serializer.instance = adjust_inventory(item=data["item"], delta=delta, reason=data["reason"], actor=self.request.user).movements.latest("id")
