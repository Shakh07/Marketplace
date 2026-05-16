from django.urls import path
from . import views

urlpatterns = [
    # API
    path('api/auth/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/users/me/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('api/addresses/', views.AddressListCreateAPIView.as_view(), name='api_addresses'),
    path('api/addresses/<int:pk>/', views.AddressDetailAPIView.as_view(), name='api_address_detail'),
    # Template
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('subscribe/', views.subscribe_newsletter, name='newsletter_subscribe'),
]
