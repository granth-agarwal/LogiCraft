from rest_framework import serializers
class SummarySerializer(serializers.Serializer):
    active_vehicles = serializers.IntegerField(); pending_shipments = serializers.IntegerField(); low_stock_items = serializers.IntegerField(); todays_bookings = serializers.IntegerField()

