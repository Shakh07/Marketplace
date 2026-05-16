from django.urls import path
from . import views

urlpatterns = [
    path('api/suppliers/', views.SupplierListAPIView.as_view(), name='api_suppliers'),
    path('api/purchase-orders/', views.PurchaseOrderListAPIView.as_view(), name='api_purchase_orders'),
]
