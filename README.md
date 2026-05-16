# NEXUS — Premium E-Commerce Platformasi

> O'zbekiston bozori uchun mo'ljallangan zamonaviy elektronika do'koni. ASUS uslubidagi premium dizayn, glassmorphism va real-time AJAX interfeysiga ega to'liq funksional e-commerce tizimi.

---

## ✨ Asosiy Imkoniyatlar

| Imkoniyat | Tavsif |
|---|---|
| 🛍 **Premium Storefront** | ASUS / ROG uslubidagi glassmorphism dizayn, micro-animatsiyalar, mega-menu |
| 🔍 **Real-time Qidiruv** | AJAX asosidagi tezkor qidiruv — sahifa yangilanmasdan ishlaydi |
| 🗂 **Kategoriya Filtri** | Noutbuklar, Monitorlar, Aksessuarlar, Gaming bo'limlari bo'yicha filtrlash |
| 🛒 **AJAX Savat** | Sahifa yangilanmasdan savatga qo'shish, badge real-time yangilanadi |
| 📦 **Buyurtma Tizimi** | Checkout, buyurtma holati kuzatuvi, chek chiqarish |
| 🖥 **Manager Paneli** | Glassmorphism uslubidagi admin panel — mahsulot, ombor, buyurtma boshqaruvi |
| 🖼 **Image Cropper** | Drag & Drop rasm yuklash + Cropper.js bilan standart formatga solish |
| 🐳 **To'liq Docker** | PostgreSQL + Gunicorn + WhiteNoise — bir buyruq bilan ishga tushadi |

---

## 🛠 Texnologiyalar

### Backend
- **Python 3.12** + **Django 6.0** + **Django REST Framework**
- **PostgreSQL 16** (production) / SQLite (development)
- **Gunicorn** — production WSGI server
- **WhiteNoise** — statik fayllar uchun

### Frontend
- **Django Templates** + **Vanilla CSS** + **Vanilla JS**
- **Glassmorphism** dizayn tizimi (`backdrop-filter: blur`)
- **Inter** + **Outfit** shriftlari (Google Fonts)
- **AJAX (Fetch API)** — partial template pattern

### DevOps
- **Docker** + **Docker Compose**
- **django-unfold** — zamonaviy admin UI
- **Pillow** — rasm qayta ishlash
- **Cropper.js** — frontend rasm qirqish

---

## 🚀 Ishga Tushirish

### Docker bilan (tavsiya etiladi)

```bash
git clone https://github.com/Kirito514/nexus-ecommerce.git
cd nexus-ecommerce
docker-compose up -d --build
```

Dastur `http://localhost:8000` da ishga tushadi.

### Lokal (development)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Test ma'lumotlarini yuklash (ixtiyoriy)

```bash
docker-compose exec web python manage.py loaddata datadump.json
```

---

## 🌐 Sahifalar

| URL | Tavsif |
|---|---|
| `http://localhost:8000/` | Bosh sahifa (hero, kategoriyalar, featured mahsulotlar) |
| `http://localhost:8000/products/` | Barcha mahsulotlar katalogi |
| `http://localhost:8000/products/?category=laptops` | Kategoriya bo'yicha filtrlash |
| `http://localhost:8000/cart/` | Savat |
| `http://localhost:8000/manager/` | Manager boshqaruv paneli |

---

## 📁 Fayl Tuzilishi

```
nexus-ecommerce/
├── apps/
│   ├── accounts/      # Foydalanuvchilar, autentifikatsiya, profil
│   ├── catalog/       # Mahsulotlar, kategoriyalar, brendlar
│   ├── orders/        # Savat, checkout, buyurtmalar
│   ├── manager/       # Admin boshqaruv paneli
│   ├── warehouse/     # Ombor va zaxira boshqaruvi
│   ├── reviews/       # Sharhlar tizimi
│   ├── returns/       # Qaytarishlar
│   └── suppliers/     # Yetkazib beruvchilar
├── templates/         # HTML shablonlar (base.html, home.html, ...)
├── static/            # CSS, JS, ikonkalar
├── media/             # Yuklangan rasmlar
├── ecommerce/         # Django loyiha sozlamalari (settings.py)
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── requirements.txt
```

---

## 👨‍💻 Muallif

**Kirito514** — Asosiy ishlab chiquvchi

---

*NEXUS — kelajak bu yerda.*
