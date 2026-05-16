from django import forms
from apps.catalog.models import Product

class ProductForm(forms.ModelForm):
    # Optional image field for adding/editing a basic thumbnail
    image = forms.ImageField(required=False, label="Mahsulot rasmi")
    
    # Inventory field (pseudo-field, handles warehouse logic in views)
    initial_stock = forms.IntegerField(required=False, initial=0, label="Ombordagi qoldiq (dona)", min_value=0)

    class Meta:
        model = Product
        fields = [
            'product_name', 'slug', 'category', 'brand', 'product_status',
            'cost_price', 'base_price', 'sale_price', 'description', 'sku', 'barcode',
            'weight', 'dimensions'
        ]

    def clean_sku(self):
        sku = self.cleaned_data.get('sku', '').strip()
        if not sku:
            # Auto-generate a unique SKU so the unique+NOT NULL constraint is satisfied
            import uuid
            sku = 'SKU-' + uuid.uuid4().hex[:8].upper()
        return sku

from apps.catalog.models import Category, HeroSection, Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'logo_url', 'website_url', 'is_active']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'description', 'image_url', 'is_active']
        
class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = [
            'eyebrow_text', 'title_line1', 'title_line2', 'title_line3',
            'subtitle', 'cta_primary_text', 'hero_image', 'is_active'
        ]

from apps.accounts.models import SiteSettings

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_domain', 'contact_email', 'contact_phone',
            'address', 'receipt_footer', 'social_instagram', 'social_telegram'
        ]
