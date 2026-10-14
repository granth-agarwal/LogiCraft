from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, StockMovementViewSet, WarehouseViewSet
router = DefaultRouter(); router.register("warehouses", WarehouseViewSet); router.register("items", InventoryItemViewSet); router.register("movements", StockMovementViewSet)
urlpatterns = router.urls

