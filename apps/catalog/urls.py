from django.urls import path
from . import views

urlpatterns = [
    # API
    path('api/categories/', views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/brands/', views.BrandListAPIView.as_view(), name='api_brands'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/wishlist/', views.WishlistListCreateAPIView.as_view(), name='api_wishlist'),
    path('api/wishlist/<int:pk>/', views.WishlistDeleteAPIView.as_view(), name='api_wishlist_delete'),
    # Template
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<slug:slug>/review/', views.submit_review_view, name='submit_review'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('help/', views.help_page_view, name='help_page'),
]
