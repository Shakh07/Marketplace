from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='manager_dashboard'),

    # Orders
    path('orders/', views.order_list, name='manager_order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='manager_order_detail'),
    path('orders/<int:order_id>/status/', views.order_update_status, name='manager_order_status'),
    path('orders/<int:order_id>/address/', views.order_update_address, name='manager_order_address'),

    # Products
    path('products/', views.product_list, name='manager_product_list'),
    path('products/add/', views.product_add, name='manager_product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='manager_product_edit'),
    path('products/<int:product_id>/toggle/', views.product_toggle_active, name='manager_product_toggle'),

    # Inventory
    path('inventory/', views.inventory_list, name='manager_inventory_list'),

    # Users
    path('users/', views.user_list, name='manager_user_list'),
    path('users/<int:user_id>/', views.user_detail, name='manager_user_detail'),
    path('users/<int:user_id>/toggle/', views.user_toggle_status, name='manager_user_toggle'),

    # CMS / Storefront
    path('storefront/', views.storefront_settings, name='manager_storefront'),
    path('categories/', views.category_list, name='manager_category_list'),
    path('categories/add/', views.category_add, name='manager_category_add'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='manager_category_edit'),

    path('brands/', views.brand_list, name='manager_brand_list'),
    path('brands/add/', views.brand_add, name='manager_brand_add'),
    path('brands/<int:brand_id>/edit/', views.brand_edit, name='manager_brand_edit'),
]
