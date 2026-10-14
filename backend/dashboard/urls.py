from django.urls import path
from .views import RevenueView, ShipmentsByStatusView, SummaryView
urlpatterns = [path("summary/", SummaryView.as_view()), path("shipments-by-status/", ShipmentsByStatusView.as_view()), path("revenue/", RevenueView.as_view())]

