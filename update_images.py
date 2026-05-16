import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from apps.catalog.models import Product, ProductImage

# Mapping of product name substrings to image filenames
mapping = {
    "ROG Strix RTX 4090": "products/rtx4090.png",
    "ROG Swift OLED": "products/swiftoled.png",
    "ProArt Studiobook": "products/proart.png",
    "Zenbook 14": "products/zenbook.png",
}

for name_sub, img_path in mapping.items():
    product = Product.objects.filter(product_name__icontains=name_sub).first()
    if product:
        print(f"Updating images for product: {product.product_name}")
        # Mark existing images as not primary or just clear them if we want to be exact
        # For this task, we'll delete existing ones to ensure our new one is shown
        product.images.all().delete()
        
        # Create new image
        ProductImage.objects.create(
            product=product,
            image_url=img_path,
            is_primary=True
        )
        print(f"Successfully added image {img_path} to {product.product_name}")
    else:
        print(f"Product containing '{name_sub}' not found.")
