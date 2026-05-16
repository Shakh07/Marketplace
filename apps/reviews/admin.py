from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Review, ReviewImage, ReviewReaction


class ReviewImageInline(TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    search_fields = ('comment', 'user__username', 'product__product_name')
    readonly_fields = ('created_at',)
    inlines = [ReviewImageInline]


@admin.register(ReviewImage)
class ReviewImageAdmin(ModelAdmin):
    list_display = ('review', 'image_url')


@admin.register(ReviewReaction)
class ReviewReactionAdmin(ModelAdmin):
    list_display = ('review', 'user', 'reaction_type', 'created_at')
    list_filter = ('reaction_type',)
    readonly_fields = ('created_at',)
