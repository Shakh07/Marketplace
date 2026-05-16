from rest_framework import generics, permissions
from .models import Warehouse, Inventory, InventoryMovement
from .serializers import WarehouseSerializer, InventorySerializer, InventoryMovementSerializer


class WarehouseListAPIView(generics.ListAPIView):
    queryset = Warehouse.objects.filter(is_active=True)
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAdminUser]


class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]


class InventoryMovementListAPIView(generics.ListAPIView):
    queryset = InventoryMovement.objects.all().order_by('-created_at')
    serializer_class = InventoryMovementSerializer
    permission_classes = [permissions.IsAdminUser]
