from rest_framework import serializers
from .models import Driver, MaintenanceRecord, Trip, Vehicle

class DriverSerializer(serializers.ModelSerializer):
    class Meta: model = Driver; fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    class Meta: model = Vehicle; fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    class Meta: model = Trip; fields = "__all__"
    def validate(self, attrs):
        vehicle = attrs.get("vehicle", getattr(self.instance, "vehicle", None))
        if vehicle and vehicle.status == Vehicle.Status.MAINTENANCE:
            raise serializers.ValidationError({"vehicle": "A vehicle in maintenance cannot be assigned to a trip."})
        return attrs

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta: model = MaintenanceRecord; fields = "__all__"

class AssignDriverSerializer(serializers.Serializer):
    driver_id = serializers.PrimaryKeyRelatedField(source="driver", queryset=Driver.objects.all())
    def validate_driver_id(self, driver):
        if driver.status != Driver.Status.AVAILABLE:
            raise serializers.ValidationError("Driver is not available.")
        return driver
