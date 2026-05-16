import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from apps.catalog.models import HeroSection

h = HeroSection.get_instance()
h.title_line1 = 'Cheksiz imkoniyat'
h.title_line2 = 'yangi qiyofada'
h.eyebrow_text = 'ASUS NEXUS — KELAJAK BU YERDA'
h.subtitle = "Eng so'nggi ROG, Zenbook va ProArt texnologiyalari — sizning mukammalligingiz uchun."
h.cta_primary_text = "Barchasini ko'rish"
h.save()

print("Hero section updated successfully in DB.")
