"""Required workflows and regressions for stock and booking capacity."""
import pytest
from tests.factories import BookingFactory, InventoryItemFactory, ScheduleFactory, VehicleFactory, WarehouseFactory

pytestmark = pytest.mark.django_db


def post(client, path, data):
    response = client.post(f"/api/v1/{path}", data, format="json")
    assert response.status_code == 201, response.data
    return response.data


def test_complete_fleet_workflow(auth, admin):
    client = auth(admin)
    vehicle = post(client, "fleet/vehicles/", {"registration_number": "UP14-DEMO", "type": "bus", "capacity_kg": "1000", "seat_capacity": 2})
    driver = post(client, "fleet/drivers/", {"profile": admin.pk, "license_number": "DEMO-LIC", "license_expiry": "2030-12-31"})
    response = client.post(f"/api/v1/fleet/vehicles/{vehicle['id']}/assign-driver/", {"driver_id": driver["id"]})
    assert response.status_code == 200
    assert response.data["current_driver"] == driver["id"]
    trip = post(client, "fleet/trips/", {"vehicle": vehicle["id"], "driver": driver["id"], "start_location": "Ghaziabad", "end_location": "Delhi", "start_time": "2030-01-01T10:00:00Z", "distance_km": "30"})
    for status in ("in_progress", "completed"):
        response = client.patch(f"/api/v1/fleet/trips/{trip['id']}/", {"status": status})
        assert response.status_code == 200
        assert response.data["status"] == status
    post(client, "fleet/maintenance/", {"vehicle": vehicle["id"], "service_date": "2030-01-02", "next_due_date": "2030-04-02", "description": "Oil change", "cost": "250.50"})
    assert client.patch(f"/api/v1/fleet/drivers/{driver['id']}/", {"status": "off_duty"}).status_code == 200
    assert client.delete(f"/api/v1/fleet/vehicles/{vehicle['id']}/").status_code == 204


def test_complete_warehouse_workflow(auth, admin):
    client = auth(admin)
    warehouse = post(client, "warehouse/warehouses/", {"name": "Depot", "address": "Ghaziabad", "capacity_units": 100, "manager": admin.pk})
    item = post(client, "warehouse/items/", {"sku": "DEMO-BOX", "name": "Boxes", "category": "Packaging", "quantity": 0, "reorder_threshold": 5, "warehouse": warehouse["id"]})
    for direction, quantity in (("inbound", 10), ("outbound", 7)):
        movement = post(client, "warehouse/movements/", {"item": item["id"], "warehouse": warehouse["id"], "movement_type": direction, "quantity": quantity, "reason": "Demo"})
        assert movement["created_by"] == admin.pk
        assert client.patch(f"/api/v1/warehouse/movements/{movement['id']}/", {"quantity": 100}).status_code == 405
    assert client.get(f"/api/v1/warehouse/items/{item['id']}/").data["quantity"] == 3
    assert client.get("/api/v1/warehouse/items/low-stock/").data[0]["id"] == item["id"]
    assert client.post("/api/v1/warehouse/movements/", {"item": item["id"], "warehouse": warehouse["id"], "movement_type": "outbound", "quantity": 4, "reason": "Too many"}).status_code == 400
    assert client.get(f"/api/v1/warehouse/items/{item['id']}/").data["quantity"] == 3
    assert client.get("/api/v1/warehouse/movements/").data["count"] == 2


@pytest.mark.parametrize("quantity", [0, -1])
def test_movement_rejects_nonpositive_quantity(auth, admin, quantity):
    item = InventoryItemFactory()
    assert auth(admin).post("/api/v1/warehouse/movements/", {"item": item.pk, "warehouse": item.warehouse_id, "movement_type": "inbound", "quantity": quantity, "reason": "Invalid"}).status_code == 400


def test_movement_rejects_wrong_warehouse(auth, admin):
    item = InventoryItemFactory()
    assert auth(admin).post("/api/v1/warehouse/movements/", {"item": item.pk, "warehouse": WarehouseFactory().pk, "movement_type": "inbound", "quantity": 1, "reason": "Invalid"}).status_code == 400
    item.refresh_from_db()
    assert item.quantity == 10


def test_complete_shipment_workflow(auth, admin):
    client = auth(admin)
    shipment = post(client, "shipments/", {"origin": "Ghaziabad", "destination": "Delhi", "vehicle": VehicleFactory().pk})
    other = post(client, "shipments/", {"origin": "Delhi", "destination": "Noida"})
    assert shipment["tracking_id"].startswith("LC-")
    assert shipment["tracking_id"] != other["tracking_id"]
    for status in ("picked_up", "in_transit", "delivered"):
        assert client.post(f"/api/v1/shipments/{shipment['id']}/update-status/", {"status": status, "note": status}).status_code == 200
    detail = client.get(f"/api/v1/shipments/{shipment['id']}/").data
    assert detail["status"] == "delivered"
    assert [event["status"] for event in detail["events"]] == ["picked_up", "in_transit", "delivered"]
    assert client.post(f"/api/v1/shipments/{shipment['id']}/update-status/", {"status": "pending"}).status_code == 400


def test_complete_scheduling_workflow(auth, admin):
    client = auth(admin)
    route = post(client, "scheduling/routes/", {"name": "City line", "stops": ["A", "B", "C"], "estimated_duration_minutes": 30})
    schedule = post(client, "scheduling/schedules/", {"route": route["id"], "vehicle": VehicleFactory(seat_capacity=1).pk, "capacity": 1, "departure_time": "2030-01-01T10:00:00Z"})
    path = f"/api/v1/scheduling/schedules/{schedule['id']}/book/"
    booking = client.post(path)
    assert booking.status_code == 201
    assert booking.data["fare"] == "20.00"
    assert client.post(path).status_code == 400
    for _ in range(2):
        assert client.post(f"/api/v1/scheduling/bookings/{booking.data['id']}/cancel/").status_code == 200
        booking = client.post(path)
        assert booking.status_code == 201
        assert booking.data["seat_number"] == 1


@pytest.mark.parametrize("seat", [0, 2])
def test_direct_booking_cannot_bypass_capacity(auth, admin, customer, seat):
    schedule = ScheduleFactory(capacity=1)
    assert auth(admin).post("/api/v1/scheduling/bookings/", {"schedule": schedule.pk, "customer": customer.pk, "seat_number": seat, "fare": "10"}).status_code == 400


def test_direct_booking_cannot_take_occupied_seat(auth, admin, customer):
    schedule = ScheduleFactory(capacity=1)
    BookingFactory(schedule=schedule, seat_number=1)
    assert auth(admin).post("/api/v1/scheduling/bookings/", {"schedule": schedule.pk, "customer": customer.pk, "seat_number": 1, "fare": "10"}).status_code == 400


def test_booking_update_cannot_exceed_capacity(auth, admin):
    booking = BookingFactory(seat_number=1, schedule=ScheduleFactory(capacity=1))
    assert auth(admin).patch(f"/api/v1/scheduling/bookings/{booking.pk}/", {"seat_number": 2}).status_code == 400


def test_schedule_and_vehicle_cannot_shrink_below_booked_seats(auth, admin):
    schedule = ScheduleFactory(capacity=2, vehicle=VehicleFactory(seat_capacity=2))
    BookingFactory(schedule=schedule, seat_number=2)
    client = auth(admin)
    assert client.patch(f"/api/v1/scheduling/schedules/{schedule.pk}/", {"capacity": 1}).status_code == 400
    assert client.patch(f"/api/v1/fleet/vehicles/{schedule.vehicle_id}/", {"seat_capacity": 1}).status_code == 400


def test_schedule_cannot_exceed_vehicle_capacity(auth, admin):
    schedule = ScheduleFactory(capacity=1, vehicle=VehicleFactory(seat_capacity=1))
    assert auth(admin).patch(f"/api/v1/scheduling/schedules/{schedule.pk}/", {"capacity": 2}).status_code == 400
