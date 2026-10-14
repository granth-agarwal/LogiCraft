from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOperations

class OperationsModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOperations]

