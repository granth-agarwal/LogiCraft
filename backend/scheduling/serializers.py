from rest_framework import serializers
from .models import Booking, Route, Schedule
class RouteSerializer(serializers.ModelSerializer):
    class Meta: model = Route; fields = "__all__"
    def validate_stops(self, value):
        if not isinstance(value, list) or len(value) < 2 or not all(isinstance(x, str) and x.strip() for x in value): raise serializers.ValidationError("Provide at least two named stops.")
        return value
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta: model = Schedule; fields = "__all__"
class BookingSerializer(serializers.ModelSerializer):
    class Meta: model = Booking; fields = "__all__"; read_only_fields = ["created_at"]
