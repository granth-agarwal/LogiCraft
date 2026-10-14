from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    allowed_roles = ()
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in self.allowed_roles)

class IsAdmin(RolePermission): allowed_roles = ("admin",)
class IsFleetManager(RolePermission): allowed_roles = ("fleet_manager",)
class IsWarehouseStaff(RolePermission): allowed_roles = ("warehouse_staff",)
class IsCustomer(RolePermission): allowed_roles = ("customer",)
class IsOperations(RolePermission): allowed_roles = ("admin", "fleet_manager", "warehouse_staff")

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "created_by", getattr(obj, "customer", getattr(obj, "recipient", None)))
        return request.user.role == "admin" or owner == request.user

