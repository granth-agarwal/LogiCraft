from rest_framework import serializers
from django.db import transaction
from .models import Booking, Route, Schedule
class RouteSerializer(serializers.ModelSerializer):
    class Meta: model = Route; fields = "__all__"
    def validate_stops(self, value):
        if not isinstance(value, list) or len(value) < 2 or not all(isinstance(x, str) and x.strip() for x in value): raise serializers.ValidationError("Provide at least two named stops.")
        return value
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta: model = Schedule; fields = "__all__"
    def validate(self, attrs):
        vehicle = attrs.get("vehicle", getattr(self.instance, "vehicle", None))
        capacity = attrs.get("capacity", getattr(self.instance, "capacity", 0))
        if capacity < 1 or (vehicle and capacity > vehicle.seat_capacity):
            raise serializers.ValidationError({"capacity": "Capacity must be between 1 and the vehicle's seat capacity."})
        if self.instance and self.instance.bookings.filter(status="booked", seat_number__gt=capacity).exists():
            raise serializers.ValidationError({"capacity": "An active booking exceeds this capacity."})
        if self.instance and "route" in attrs and attrs["route"] != self.instance.route and self.instance.bookings.filter(status="booked").exists():
            raise serializers.ValidationError({"route": "Cancel active bookings before changing route."})
        return attrs
class BookingSerializer(serializers.ModelSerializer):
    class Meta: model = Booking; fields = "__all__"; read_only_fields = ["created_at", "active_seat"]
    def validate_fare(self, value):
        if value < 0:
            raise serializers.ValidationError("Fare cannot be negative.")
        return value
    def check_capacity(self, attrs):
        schedule = attrs.get("schedule", getattr(self.instance, "schedule", None))
        schedule = Schedule.objects.select_for_update().get(pk=schedule.pk)
        seat = attrs.get("seat_number", getattr(self.instance, "seat_number", 0))
        if not 1 <= seat <= min(schedule.capacity, schedule.vehicle.seat_capacity):
            raise serializers.ValidationError({"seat_number": "Seat exceeds capacity."})
        if attrs.get("status", getattr(self.instance, "status", "booked")) == "booked":
            active = schedule.bookings.filter(status="booked")
            if self.instance:
                active = active.exclude(pk=self.instance.pk)
            if active.count() >= schedule.capacity or active.filter(seat_number=seat).exists():
                raise serializers.ValidationError({"seat_number": "Seat unavailable or schedule fully booked."})
    @transaction.atomic
    def create(self, validated_data):
        self.check_capacity(validated_data)
        return super().create(validated_data)
    @transaction.atomic
    def update(self, instance, validated_data):
        self.check_capacity(validated_data)
        return super().update(instance, validated_data)
