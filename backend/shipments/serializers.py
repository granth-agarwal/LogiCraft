from rest_framework import serializers
from .models import Shipment, ShipmentEvent
from .services import TRANSITIONS
class ShipmentEventSerializer(serializers.ModelSerializer):
    class Meta: model = ShipmentEvent; fields = "__all__"; read_only_fields = ["timestamp"]
    def create(self, validated_data): raise serializers.ValidationError("Shipment events are append-only through update-status.")
    def update(self, instance, validated_data): raise serializers.ValidationError("Shipment events are append-only.")
class ShipmentSerializer(serializers.ModelSerializer):
    events = ShipmentEventSerializer(many=True, read_only=True)
    class Meta: model = Shipment; fields = "__all__"; read_only_fields = ["tracking_id", "created_by", "created_at", "status"]
class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Shipment.Status.choices); note = serializers.CharField(required=False, allow_blank=True)
    def validate_status(self, value):
        shipment = self.context["shipment"]
        if value not in TRANSITIONS[shipment.status]: raise serializers.ValidationError(f"Cannot transition from {shipment.status} to {value}.")
        return value

