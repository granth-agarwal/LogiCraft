from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, MaintenanceRecordViewSet, TripViewSet, VehicleViewSet
router = DefaultRouter()
router.register("vehicles", VehicleViewSet); router.register("drivers", DriverViewSet); router.register("trips", TripViewSet); router.register("maintenance", MaintenanceRecordViewSet)
urlpatterns = router.urls

