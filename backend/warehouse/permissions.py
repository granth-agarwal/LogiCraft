from common.permissions import RolePermission
class CanManageWarehouse(RolePermission): allowed_roles = ("admin", "warehouse_staff")
__all__ = ["CanManageWarehouse"]
