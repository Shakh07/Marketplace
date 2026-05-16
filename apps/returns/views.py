from rest_framework import generics, permissions
from .models import Return
from .serializers import ReturnSerializer


class ReturnListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Return.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
