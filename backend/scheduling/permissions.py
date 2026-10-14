from common.permissions import IsOwnerOrAdmin, RolePermission
class CanManageScheduling(RolePermission): allowed_roles = ("admin", "fleet_manager")
__all__ = ["CanManageScheduling", "IsOwnerOrAdmin"]
