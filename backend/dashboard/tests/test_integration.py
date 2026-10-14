import pytest
from tests.factories import BookingFactory,InventoryItemFactory,ScheduleFactory,ShipmentFactory,VehicleFactory
pytestmark=pytest.mark.django_db
def test_summary_aggregates_all_domains(auth,admin):
    VehicleFactory(status="active"); ShipmentFactory(status="pending"); InventoryItemFactory(quantity=1,reorder_threshold=2); BookingFactory(schedule=ScheduleFactory(vehicle=VehicleFactory(status="idle"))); data=auth(admin).get("/api/v1/dashboard/summary/").data; assert data=={"active_vehicles":1,"pending_shipments":1,"low_stock_items":1,"todays_bookings":1}
