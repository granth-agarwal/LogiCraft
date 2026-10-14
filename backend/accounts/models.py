from django.db import models

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        FLEET_MANAGER = "fleet_manager", "Fleet manager"
        WAREHOUSE_STAFF = "warehouse_staff", "Warehouse staff"
        CUSTOMER = "customer", "Customer"
    supabase_user_id = models.UUIDField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=32, blank=True)
    warehouse = models.ForeignKey("warehouse.Warehouse", null=True, blank=True, on_delete=models.SET_NULL, related_name="staff")
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def is_authenticated(self): return True
    @property
    def is_anonymous(self): return False
    def __str__(self): return self.full_name or str(self.supabase_user_id)

