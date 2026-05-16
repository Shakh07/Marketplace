from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

# Allowed image extensions for uploads
_IMG_EXTS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
_img_validator = [FileExtensionValidator(allowed_extensions=_IMG_EXTS)]


class HeroSection(models.Model):
    """Singleton model for controlling the landing page hero section from admin."""
    title_line1 = models.CharField(max_length=100, default="Cheksiz imkoniyat", help_text="Hero sarlavha 1-qator")
    title_line2 = models.CharField(max_length=100, default="yangi qiyofada", help_text="Hero sarlavha 2-qator")
    title_line3 = models.CharField(max_length=100, default="ASUS bilan.", help_text="Hero sarlavha 3-qator")
    eyebrow_text = models.CharField(max_length=150, default="ASUS NEXUS — KELAJAK BU YERDA", help_text="Sarlavha ustidagi kichik matn")
    subtitle = models.TextField(default="Eng so'nggi ROG, Zenbook va ProArt texnologiyalari — sizning mukammalligingiz uchun.", help_text="Sarlavha ostidagi tavsif")
    cta_primary_text = models.CharField(max_length=60, default="Barchasini ko'rish")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, validators=_img_validator, help_text="Hero qismdagi chiroyli rasm (tavsiya: 1200x900)")
    badge_text = models.CharField(max_length=60, default="🔥 Top Sotuvchi", blank=True, help_text="Rasm ustidagi badge matni (bo'sh qoldirsa ko'rinmaydi)")
    floating_card_title = models.CharField(max_length=80, default="Rasmiy mahsulotlar", blank=True)
    floating_card_sub = models.CharField(max_length=80, default="Kafolatlangan sifat", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hero_section'
        verbose_name = 'Hero bo\'limi'
        verbose_name_plural = 'Hero bo\'limi'

    def __str__(self):
        return f"Hero: {self.title_line1} {self.title_line2}"

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance, creating one if it doesn't exist."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Category(models.Model):
    """Product categories with hierarchical (self-referencing) structure."""
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories'
    )
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    image_url = models.ImageField(upload_to='categories/', blank=True, null=True, validators=_img_validator)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['category_name']

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    """Product brands."""
    brand_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo_url = models.ImageField(upload_to='brands/', blank=True, null=True, validators=_img_validator)
    website_url = models.URLField(max_length=255, blank=True)
    country_of_origin = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'brands'
        ordering = ['brand_name']

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    """Main product table."""

    class ProductStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'
        DISCONTINUED = 'discontinued', 'Discontinued'

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    barcode = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True)
    product_status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT)
    is_featured = models.BooleanField(default=False)
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.product_name

    @property
    def current_price(self):
        """Return sale_price if available, otherwise base_price."""
        return self.sale_price if self.sale_price else self.base_price

    @property
    def discount_percentage(self):
        if self.sale_price and self.base_price > 0:
            return int(((self.base_price - self.sale_price) / self.base_price) * 100)
        return 0

    @property
    def total_stock(self):
        """Return the sum of quantity_available across all connected warehouse inventory."""
        from django.db.models import Sum
        ts = self.inventory.aggregate(Sum('quantity_available'))['quantity_available__sum']
        return ts or 0


class ProductVariant(models.Model):
    """Product variants (size, color, etc.)."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, blank=True)
    variant_name = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    image_url = models.ImageField(upload_to='variants/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variants'

    def __str__(self):
        return f"{self.product.product_name} — {self.variant_name}"


class VariantAttribute(models.Model):
    """Attributes for product variants."""
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=50)
    attribute_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'variant_attributes'

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"


class ProductImage(models.Model):
    """Product images."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, null=True, blank=True, related_name='variant_images')
    image_url = models.ImageField(upload_to='products/', validators=_img_validator)
    thumbnail_url = models.ImageField(upload_to='products/thumbs/', blank=True, null=True, validators=_img_validator)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return f"Image for {self.product.product_name}"


class ProductAttribute(models.Model):
    """Category-specific attributes (e.g. Screen Size for Electronics)."""

    class AttributeType(models.TextChoices):
        TEXT = 'text', 'Text'
        NUMBER = 'number', 'Number'
        BOOLEAN = 'boolean', 'Boolean'
        SELECT = 'select', 'Select'
        MULTISELECT = 'multiselect', 'Multi-Select'

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_type = models.CharField(max_length=15, choices=AttributeType.choices, default=AttributeType.TEXT)
    is_filterable = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_attributes'

    def __str__(self):
        return f"{self.attribute_name} ({self.category.category_name})"


class ProductAttributeValue(models.Model):
    """Values for product attributes."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_attribute_values'

    def __str__(self):
        return f"{self.attribute.attribute_name}: {self.value}"


class Tag(models.Model):
    """Product tags."""
    tag_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.tag_name


class ProductTag(models.Model):
    """Many-to-many relationship between products and tags."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        db_table = 'product_tags'
        unique_together = ('product', 'tag')

    def __str__(self):
        return f"{self.product.product_name} — {self.tag.tag_name}"


class ProductQuestion(models.Model):
    """Questions asked by users about products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_questions')
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Q: {self.question[:50]}..."


class Wishlist(models.Model):
    """User wishlists — NEW table not in original schema."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlists'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} — {self.product.product_name}"
