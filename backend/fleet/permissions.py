from common.permissions import RolePermission
class CanManageFleet(RolePermission): allowed_roles = ("admin", "fleet_manager")
__all__ = ["CanManageFleet"]
