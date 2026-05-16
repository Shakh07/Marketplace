from django.urls import path
from . import views

urlpatterns = [
    path('api/returns/', views.ReturnListCreateAPIView.as_view(), name='api_returns'),
]
