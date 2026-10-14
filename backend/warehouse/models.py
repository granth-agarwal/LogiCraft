from django.db import models
from django.db.models import Q

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    capacity_units = models.PositiveIntegerField()
    manager = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT, related_name="managed_warehouses")
    def __str__(self): return self.name

class InventoryItem(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=128)
    quantity = models.IntegerField(default=0)
    reorder_threshold = models.PositiveIntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="items")
    class Meta:
        constraints = [models.CheckConstraint(condition=Q(quantity__gte=0), name="inventory_quantity_nonnegative")]
    def __str__(self): return f"{self.sku} — {self.name}"

class StockMovement(models.Model):
    class Type(models.TextChoices):
        INBOUND = "inbound", "Inbound"
        OUTBOUND = "outbound", "Outbound"
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock_movements")
    movement_type = models.CharField(max_length=16, choices=Type.choices)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    created_by = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT, related_name="stock_movements")
    created_at = models.DateTimeField(auto_now_add=True)

