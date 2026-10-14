from rest_framework import serializers
from .models import InventoryItem, StockMovement, Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta: model = Warehouse; fields = "__all__"
class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta: model = InventoryItem; fields = "__all__"
    def validate_quantity(self, value):
        if value < 0: raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
class StockMovementSerializer(serializers.ModelSerializer):
    class Meta: model = StockMovement; fields = "__all__"; read_only_fields = ["created_at"]
class StockAdjustmentSerializer(serializers.Serializer):
    delta = serializers.IntegerField()
    reason = serializers.CharField(max_length=255)
    def validate_delta(self, value):
        if value == 0: raise serializers.ValidationError("Adjustment cannot be zero.")
        return value

