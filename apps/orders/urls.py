from django.urls import path
from . import views

urlpatterns = [
    # API
    path('api/orders/', views.OrderListAPIView.as_view(), name='api_orders'),
    path('api/orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/cart/', views.CartListAPIView.as_view(), name='api_cart'),
    # Template
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:order_id>/receipt/', views.order_receipt_print, name='order_receipt_print'),
]
