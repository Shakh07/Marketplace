import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from apps.catalog.models import Product, Category, Brand
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

# Create Brand
brand_asus, _ = Brand.objects.get_or_create(brand_name='ASUS')

# Categories mapping
cats = {
    'Laptops': 'laptops',
    'Gaming': 'gaming',
    'Monitors': 'monitors',
    'Desktops': 'desktops',
    'Components': 'components',
    'Creators': 'creators',
    'Business': 'business'
}

for name, slug in cats.items():
    c, created = Category.objects.get_or_create(category_name=name, slug=slug)
    if created:
        print(f"Created category: {name}")

# Create some products
products = [
    ('ROG Zephyrus G16', 'gaming', 24000000, True),
    ('ROG Strix Scar 18', 'gaming', 35000000, False),
    ('Zenbook 14 OLED', 'laptops', 14000000, True),
    ('Vivobook S 15', 'laptops', 9000000, False),
    ('ProArt Studiobook 16', 'creators', 28000000, True),
    ('ExpertBook B9', 'business', 18000000, False),
    ('ROG Swift OLED PG32UCDM', 'monitors', 12000000, True),
    ('TUF Gaming VG279QM', 'monitors', 4500000, False),
    ('ASUS Prime Z790-A', 'components', 3500000, False),
    ('ROG Strix RTX 4090', 'components', 22000000, True),
]

for i, (name, cat_slug, price, featured) in enumerate(products):
    cat = Category.objects.get(slug=cat_slug)
    slug = name.lower().replace(' ', '-')
    Product.objects.get_or_create(
        slug=slug,
        defaults={
            'product_name': name,
            'base_price': price,
            'brand': brand_asus,
            'category': cat,
            'product_status': 'active',
            'is_featured': featured,
            'seller': admin_user,
            'sku': f'ASUS-{cat_slug[:3].upper()}-{i:04d}'
        }
    )
from apps.catalog.models import HeroSection
h = HeroSection.get_instance()
h.title_line1 = 'Cheksiz imkoniyat'
h.title_line2 = 'yangi qiyofada'
h.eyebrow_text = 'ASUS NEXUS — KELAJAK BU YERDA'
h.subtitle = "Eng so'nggi ROG, Zenbook va ProArt texnologiyalari — sizning mukammalligingiz uchun."
h.cta_primary_text = "Barchasini ko'rish"
h.save()
print("Hero section updated.")

print("Finished seeding products.")
