from dashboard.serializers import SummarySerializer
def test_summary_contract(): assert SummarySerializer(data={"active_vehicles":1,"pending_shipments":2,"low_stock_items":3,"todays_bookings":4}).is_valid()

