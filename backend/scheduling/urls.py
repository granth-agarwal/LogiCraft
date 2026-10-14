from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, RouteViewSet, ScheduleViewSet
router = DefaultRouter(); router.register("routes", RouteViewSet); router.register("schedules", ScheduleViewSet); router.register("bookings", BookingViewSet, basename="booking")
urlpatterns = router.urls

