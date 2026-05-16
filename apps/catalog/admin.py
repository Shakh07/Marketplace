from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import (
    Category, Brand, Product, ProductVariant, VariantAttribute,
    ProductImage, ProductAttribute, ProductAttributeValue,
    Tag, ProductTag, ProductQuestion, Wishlist, HeroSection
)


@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ('title_line1', 'title_line2', 'is_active')
    fieldsets = (
        ('Sarlavhalar', {'fields': ('eyebrow_text', 'title_line1', 'title_line2', 'title_line3', 'subtitle', 'cta_primary_text')}),
        ('Hero Rasm va Badge', {'fields': ('hero_image', 'badge_text', 'floating_card_title', 'floating_card_sub')}),
        ('Holat', {'fields': ('is_active',)}),
    )

    def has_add_permission(self, request):
        return not HeroSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1


class VariantAttributeInline(TabularInline):
    model = VariantAttribute
    extra = 1


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('category_name', 'parent_category', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent_category')
    search_fields = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('brand_name', 'country_of_origin', 'is_active', 'created_at')
    list_filter = ('is_active', 'country_of_origin')
    search_fields = ('brand_name',)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('product_name', 'category', 'brand', 'base_price', 'sale_price', 'product_status', 'is_featured', 'average_rating')
    list_filter = ('product_status', 'is_featured', 'category', 'brand')
    search_fields = ('product_name', 'sku', 'barcode', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('total_sales', 'total_revenue', 'average_rating', 'created_at', 'updated_at')


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ('product', 'variant_name', 'sku', 'price_adjustment', 'stock_quantity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('variant_name', 'sku')
    inlines = [VariantAttributeInline]


@admin.register(VariantAttribute)
class VariantAttributeAdmin(ModelAdmin):
    list_display = ('variant', 'attribute_name', 'attribute_value')
    search_fields = ('attribute_name', 'attribute_value')


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ('product', 'is_primary')
    list_filter = ('is_primary',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = ('attribute_name', 'category', 'attribute_type', 'is_filterable')
    list_filter = ('attribute_type', 'is_filterable', 'category')


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('value',)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('tag_name', 'slug')
    prepopulated_fields = {'slug': ('tag_name',)}


@admin.register(ProductTag)
class ProductTagAdmin(ModelAdmin):
    list_display = ('product', 'tag')


@admin.register(ProductQuestion)
class ProductQuestionAdmin(ModelAdmin):
    list_display = ('product', 'user', 'question', 'created_at')
    search_fields = ('question',)
    readonly_fields = ('created_at',)


@admin.register(Wishlist)
class WishlistAdmin(ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    readonly_fields = ('added_at',)
