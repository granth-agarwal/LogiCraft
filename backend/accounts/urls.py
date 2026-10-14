from django.urls import path
from .views import MeView, UserListView
urlpatterns = [path("profile/me/", MeView.as_view()), path("users/", UserListView.as_view())]

