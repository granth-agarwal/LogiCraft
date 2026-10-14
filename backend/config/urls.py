from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/fleet/", include("fleet.urls")),
    path("api/v1/warehouse/", include("warehouse.urls")),
    path("api/v1/shipments/", include("shipments.urls")),
    path("api/v1/scheduling/", include("scheduling.urls")),
    path("api/v1/dashboard/", include("dashboard.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
]

