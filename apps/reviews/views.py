from rest_framework import generics, permissions
from .models import Review, ReviewReaction
from .serializers import ReviewSerializer, ReviewReactionSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            return Review.objects.filter(product_id=product_id, is_approved=True)
        return Review.objects.filter(is_approved=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewReactionCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
