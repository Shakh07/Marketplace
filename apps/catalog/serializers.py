from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductVariant, ProductImage,
    Tag, ProductQuestion, Wishlist
)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'parent_category', 'category_name', 'description', 'slug', 'image_url', 'is_active', 'subcategories')

    def get_subcategories(self, obj):
        children = obj.subcategories.filter(is_active=True)
        return CategorySerializer(children, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image_url', 'thumbnail_url', 'is_primary')


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'variant_name', 'sku', 'price_adjustment', 'stock_quantity', 'image_url', 'is_active')


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    brand_name = serializers.CharField(source='brand.brand_name', read_only=True, default='')
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'slug', 'base_price', 'sale_price',
                  'product_status', 'is_featured', 'average_rating', 'category_name',
                  'brand_name', 'primary_image', 'discount_percentage')

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first()
        if img and img.image_url:
            return img.image_url.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductQuestionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductQuestion
        fields = ('id', 'product', 'user', 'username', 'question', 'created_at')
        read_only_fields = ('user',)


class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'product_detail', 'added_at')
        read_only_fields = ('user',)
