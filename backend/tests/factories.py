import uuid
from datetime import timedelta
import factory
from django.utils import timezone
from accounts.models import Profile
from fleet.models import Driver, MaintenanceRecord, Trip, Vehicle
from notifications.models import Notification
from scheduling.models import Booking, Route, Schedule
from shipments.models import Shipment, ShipmentEvent
from warehouse.models import InventoryItem, StockMovement, Warehouse

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta: model = Profile
    supabase_user_id = factory.LazyFunction(uuid.uuid4); full_name = factory.Sequence(lambda n:f"User {n}"); role = Profile.Role.ADMIN
class WarehouseFactory(factory.django.DjangoModelFactory):
    class Meta: model = Warehouse
    name = factory.Sequence(lambda n:f"Warehouse {n}"); address = "1 Depot Way"; capacity_units = 1000; manager = factory.SubFactory(ProfileFactory)
class DriverFactory(factory.django.DjangoModelFactory):
    class Meta: model = Driver
    profile = factory.SubFactory(ProfileFactory); license_number = factory.Sequence(lambda n:f"LIC-{n}"); license_expiry = factory.LazyFunction(lambda:timezone.localdate()+timedelta(days=365)); status = Driver.Status.AVAILABLE
class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta: model = Vehicle
    registration_number = factory.Sequence(lambda n:f"LC-{n:04}"); type = Vehicle.Type.TRUCK; capacity_kg = 1000; status = Vehicle.Status.ACTIVE
class TripFactory(factory.django.DjangoModelFactory):
    class Meta: model = Trip
    vehicle = factory.SubFactory(VehicleFactory); driver = factory.SubFactory(DriverFactory); start_location = "A"; end_location = "B"; start_time = factory.LazyFunction(timezone.now); distance_km = 20
class MaintenanceRecordFactory(factory.django.DjangoModelFactory):
    class Meta: model = MaintenanceRecord
    vehicle = factory.SubFactory(VehicleFactory); service_date = factory.LazyFunction(timezone.localdate); next_due_date = factory.LazyFunction(lambda:timezone.localdate()+timedelta(days=90)); description = "Service"; cost = 100
class InventoryItemFactory(factory.django.DjangoModelFactory):
    class Meta: model = InventoryItem
    sku = factory.Sequence(lambda n:f"SKU-{n}"); name = "Carton"; category = "Packaging"; quantity = 10; reorder_threshold = 3; warehouse = factory.SubFactory(WarehouseFactory)
class StockMovementFactory(factory.django.DjangoModelFactory):
    class Meta: model = StockMovement
    item = factory.SubFactory(InventoryItemFactory); warehouse = factory.SelfAttribute("item.warehouse"); movement_type = StockMovement.Type.INBOUND; quantity = 1; reason = "Restock"; created_by = factory.SubFactory(ProfileFactory)
class ShipmentFactory(factory.django.DjangoModelFactory):
    class Meta: model = Shipment
    origin = "A"; destination = "B"; quantity = 1; created_by = factory.SubFactory(ProfileFactory)
class ShipmentEventFactory(factory.django.DjangoModelFactory):
    class Meta: model = ShipmentEvent
    shipment = factory.SubFactory(ShipmentFactory); status = Shipment.Status.PICKED_UP; note = "Collected"
class RouteFactory(factory.django.DjangoModelFactory):
    class Meta: model = Route
    name = factory.Sequence(lambda n:f"Route {n}"); stops = ["A","B","C"]; estimated_duration_minutes = 60
class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta: model = Schedule
    route = factory.SubFactory(RouteFactory); departure_time = factory.LazyFunction(timezone.now); vehicle = factory.SubFactory(VehicleFactory); capacity = 2
class BookingFactory(factory.django.DjangoModelFactory):
    class Meta: model = Booking
    schedule = factory.SubFactory(ScheduleFactory); customer = factory.SubFactory(ProfileFactory, role=Profile.Role.CUSTOMER); seat_number = factory.Sequence(lambda n:n+1); fare = 20
class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta: model = Notification
    recipient = factory.SubFactory(ProfileFactory); message = "Update"; type = Notification.Type.SHIPMENT_UPDATE
