from django.urls import path
from . import views

urlpatterns = [
    path('api/warehouses/', views.WarehouseListAPIView.as_view(), name='api_warehouses'),
    path('api/inventory/', views.InventoryListAPIView.as_view(), name='api_inventory'),
    path('api/inventory/movements/', views.InventoryMovementListAPIView.as_view(), name='api_inventory_movements'),
]
