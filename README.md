# NEXUS Marketplace

**O'zbekiston bozori uchun Django asosida qurilgan to'liq e-commerce tizimi.**

Muallif: **Shohruh** · [github.com/Shakh07/Marketplace](https://github.com/Shakh07/Marketplace)

---

## Loyiha haqida

NEXUS — mahsulotlarni ko'rish, savatga solish va buyurtma berishgacha bo'lgan to'liq jarayonni qamrab oluvchi onlayn do'kon. Ikkita tomoni bor: xaridorlar uchun ochiq storefront va operatorlar uchun yopiq manager panel.

Vaqt zonasi — `Asia/Tashkent`. Ma'lumotlar bazasi: PostgreSQL. Interfeys tili: O'zbek + Ingliz.

---

## Texnologiyalar

**Backend:** Python 3.12, Django 6.0.3, Django REST Framework 3.17.1  
**Ma'lumotlar bazasi:** PostgreSQL 16 (production), SQLite (local)  
**Frontend:** Django Templates, Vanilla CSS, Vanilla JS, Fetch API  
**Dizayn:** Glassmorphism — `backdrop-filter: blur`, shaffof kartalar  
**Shriftlar:** Inter + Outfit (Google Fonts)  
**Infra:** Docker, Docker Compose, Gunicorn, WhiteNoise  

Barcha kutubxonalar `requirements.txt` da to'liq ko'rsatilgan.

---

## Ishga tushirish

### Docker (tavsiya etiladi)

```bash
git clone https://github.com/Shakh07/Marketplace.git
cd Marketplace
docker-compose up --build -d
```

Ochiladi: `http://localhost:8000`

### Lokal muhitda

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> **Eslatma:** `.env` faylida `DATABASE_URL` yoki alohida `DB_NAME`, `DB_USER`, `DB_PASSWORD` o'zgaruvchilarini belgilash kerak. Aks holda loyiha `nexus_db` nomli lokal PostgreSQL bazasiga ulanishga harakat qiladi.

---

## Tuzilishi

```
Marketplace/
├── apps/
│   ├── accounts/    # Foydalanuvchi tizimi
│   ├── catalog/     # Mahsulotlar, kategoriyalar, brendlar
│   ├── orders/      # Savat va buyurtmalar
│   ├── manager/     # Operator paneli
│   ├── warehouse/   # Ombor zaxirasi
│   ├── reviews/     # Sharhlar
│   ├── returns/     # Qaytarishlar
│   └── suppliers/   # Ta'minotchilar
├── templates/       # Barcha HTML shablonlar
├── static/          # CSS va JS fayllar
├── ecommerce/       # Django sozlamalari (settings, urls, wsgi)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Asosiy sahifalar

| URL | Nima ko'rinadi |
|---|---|
| `/` | Bosh sahifa |
| `/products/` | Barcha mahsulotlar |
| `/products/<slug>/` | Mahsulot kartasi |
| `/cart/` | Savat |
| `/checkout/` | Buyurtma berish |
| `/orders/` | Buyurtmalar tarixi |
| `/manager/` | Operator paneli |
| `/admin/` | Django admin (Unfold) |

---

## Muallif

**Shohruh** · [@Shakh07](https://github.com/Shakh07)
