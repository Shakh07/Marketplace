from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

_img_validator = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp','gif'])]


class Review(models.Model):
    """Product reviews by users."""
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.product.product_name} ({self.rating}★)"


class ReviewImage(models.Model):
    """Images attached to reviews."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='reviews/', validators=_img_validator)

    class Meta:
        db_table = 'review_images'

    def __str__(self):
        return f"Image for review #{self.review.id}"


class ReviewReaction(models.Model):
    """User reactions to reviews (helpful/unhelpful)."""

    class ReactionType(models.TextChoices):
        HELPFUL = 'helpful', 'Helpful'
        UNHELPFUL = 'unhelpful', 'Unhelpful'

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_reactions')
    reaction_type = models.CharField(max_length=10, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_reactions'
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} — {self.reaction_type}"


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.product
    # calculate average of approved reviews
    avg = product.reviews.filter(is_approved=True).aggregate(average=Avg('rating'))['average']
    if avg is None:
        avg = 0
    product.average_rating = round(avg, 2)
    product.save(update_fields=['average_rating'])
