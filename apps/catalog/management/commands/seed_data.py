import random
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from django.utils.text import slugify
from apps.accounts.models import CustomUser
from apps.catalog.models import Category, Brand, Product, ProductImage, ProductVariant
from apps.orders.models import Order
from apps.reviews.models import Review

class Command(BaseCommand):
    help = 'Tizimni Apple mahsulotlari bilan to\'ldirish (Seeding)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Apple Seeding boshlandi...')

        # Flush old products
        self.stdout.write('Eski ma\'lumotlar o\'chirilmoqda...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()

        # 1. Categories
        categories_data = [
            'Mac', 'iPad', 'iPhone', 'Watch', 'AirPods', 'TV & Home', 'Accessories'
        ]
        created_categories = {}
        for name in categories_data:
            cat_slug = slugify(name)
            cat, _ = Category.objects.get_or_create(category_name=name, defaults={'slug': cat_slug})
            created_categories[name] = cat
            self.stdout.write(f'Kategoriya yaratildi: {name}')

        # 2. Brands
        apple_brand, _ = Brand.objects.get_or_create(brand_name='Apple')

        # 3. Users
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin_user = CustomUser.objects.get(username='admin')

        # 4. Apple Products Data
        apple_products = [
            {
                'name': 'iPhone 16 Pro',
                'cat': 'iPhone',
                'price': 999,
                'desc': 'Titanium. So strong. So light. So Pro.',
                'image': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'iPhone 16',
                'cat': 'iPhone',
                'price': 799,
                'desc': 'New camera. New design. Newphoria.',
                'image': 'https://images.unsplash.com/photo-1695048065099-231a44eebff5?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'MacBook Air M3',
                'cat': 'Mac',
                'price': 1099,
                'desc': 'Lean. Mean. M3 machine.',
                'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'MacBook Pro 16-inch',
                'cat': 'Mac',
                'price': 2499,
                'desc': 'Mind-blowing. Head-turning.',
                'image': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'Apple Watch Ultra 2',
                'cat': 'Watch',
                'price': 799,
                'desc': 'Next level adventure.',
                'image': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'Apple Watch Series 9',
                'cat': 'Watch',
                'price': 399,
                'desc': 'Smarter. Brighter. Mightier.',
                'image': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'AirPods Pro 2',
                'cat': 'AirPods',
                'price': 249,
                'desc': 'Adaptive Audio. Now playing.',
                'image': 'https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?auto=format&fit=crop&q=80&w=800'
            },
            {
                'name': 'iPad Pro M4',
                'cat': 'iPad',
                'price': 999,
                'desc': 'Thinner. Lighter. More Pro.',
                'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&q=80&w=800'
            }
        ]

        # In this approach I'll use simple generated color boxes for downloading speed, 
        # but the actual landing page will use high-res unsplash backgrounds directly in CSS/HTML!
        colors = ['#1d1d1f', '#f5f5f7', '#0071e3', '#c9a84c']

        for item in apple_products:
            p_name = item['name']
            p_slug = slugify(p_name)
            
            product, created = Product.objects.get_or_create(
                slug=p_slug,
                defaults={
                    'category': created_categories[item['cat']],
                    'brand': apple_brand,
                    'seller': admin_user,
                    'product_name': p_name,
                    'sku': str(random.randint(100000, 999999)),
                    'description': item['desc'],
                    'base_price': item['price'],
                    'is_featured': True,
                    'total_sales': random.randint(10, 500),
                    'average_rating': random.uniform(4.5, 5.0)
                }
            )

            if created:
                # Generate a minimal Image using Pillow so it doesn't break image refs
                color = random.choice(colors)
                img = Image.new('RGB', (800, 800), color=color)
                # No text or complex things to keep it fast
                b = BytesIO()
                img.save(b, 'JPEG')
                
                p_img = ProductImage(product=product, is_primary=True)
                p_img.image_url.save(f"apple_{product.id}.jpg", ContentFile(b.getvalue()))
                p_img.save()
                
            self.stdout.write(f'Mahsulot tayyor: {p_name}')

        self.stdout.write(self.style.SUCCESS('Sayt Apple mahsulotlari bilan muvaffaqiyatli to\'ldirildi!'))
