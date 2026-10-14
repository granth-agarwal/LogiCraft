from django.db import models

class Driver(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ON_TRIP = "on_trip", "On trip"
        OFF_DUTY = "off_duty", "Off duty"
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name="driver_records")
    license_number = models.CharField(max_length=64, unique=True)
    license_expiry = models.DateField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.AVAILABLE)
    def __str__(self): return self.license_number

class Vehicle(models.Model):
    class Type(models.TextChoices):
        TRUCK = "truck", "Truck"
        VAN = "van", "Van"
        BUS = "bus", "Bus"
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        MAINTENANCE = "maintenance", "Maintenance"
        IDLE = "idle", "Idle"
        RETIRED = "retired", "Retired"
    registration_number = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    capacity_kg = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IDLE)
    current_driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_vehicles")
    def __str__(self): return self.registration_number

class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="trips")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="trips")
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.SCHEDULED)
    route_points = models.JSONField(default=list, blank=True)

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_records")
    service_date = models.DateField()
    next_due_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)

