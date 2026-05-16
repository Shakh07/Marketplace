import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from apps.catalog.models import Product

products = Product.objects.all()
for p in products:
    print(f"ID: {p.id}, Name: {p.product_name}")
