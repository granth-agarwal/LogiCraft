from django.urls import path
from .views import MeView, UserListView
from .local_auth import session
urlpatterns = [path("profile/me/", MeView.as_view()), path("users/", UserListView.as_view()), path("auth/session/", session)]

