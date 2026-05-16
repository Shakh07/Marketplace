from django.urls import path
from . import views

urlpatterns = [
    path('api/reviews/', views.ReviewListCreateAPIView.as_view(), name='api_reviews'),
    path('api/reviews/product/<int:product_id>/', views.ReviewListCreateAPIView.as_view(), name='api_product_reviews'),
    path('api/reviews/react/', views.ReviewReactionCreateAPIView.as_view(), name='api_review_reaction'),
]
