from rest_framework import serializers
from .models import Review, ReviewImage, ReviewReaction


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ('id', 'image_url')


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'username', 'order', 'rating', 'comment', 'is_approved', 'images', 'created_at')
        read_only_fields = ('user', 'is_approved')


class ReviewReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReaction
        fields = ('id', 'review', 'reaction_type', 'created_at')
        read_only_fields = ('user',)
