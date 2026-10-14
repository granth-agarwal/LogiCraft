from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
from common.permissions import IsAdmin

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self): return self.request.user

class UserListView(generics.ListAPIView):
    queryset = Profile.objects.select_related("warehouse").order_by("id")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_fields = ["role"]
    search_fields = ["full_name", "phone"]
