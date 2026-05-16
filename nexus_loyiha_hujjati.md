# 📄 NEXUS Marketplace — Loyiha Texnik Hujjati

> **Muallif:** Shohruh  
> **GitHub:** [@Shakh07](https://github.com/Shakh07)  
> **Loyiha:** [github.com/Shakh07/Marketplace](https://github.com/Shakh07/Marketplace)  
> **Sana:** 2026-yil, May

---

## 1. Loyihaga Umumiy Nazar

**NEXUS** — O'zbekiston bozori uchun qurilgan to'liq funksional **premium elektronika do'koni** platformasi. Loyiha ikkita asosiy qismdan iborat:

- **Storefront** — xaridorlar uchun: mahsulotlarni ko'rish, filtrlash, savatga qo'shish, buyurtma berish.
- **Manager Panel** — adminlar uchun: buyurtmalar, mahsulotlar, ombor, foydalanuvchilar, statistika.

Dizayn **ASUS / ROG** uslubida — glassmorphism effektlari, neon ko'k aksentlar, premium tipografiya va silliq animatsiyalar.

---

## 2. Texnologiyalar Steki

### 2.1 Dasturlash Tillari

| Til | Ishlatilgan joy | Vazifa |
|---|---|---|
| Python 3.12 | Backend | Asosiy server logikasi (Django) |
| HTML5 | Templates | Sahifa tuzilishi |
| CSS3 | Dizayn | Glassmorphism, animatsiyalar, rang tizimi |
| JavaScript ES6+ | Frontend | AJAX, real-time UI, savat, mega-menu |
| SQL | Ma'lumotlar bazasi | Django ORM orqali PostgreSQL |
| Bash | DevOps | `entrypoint.sh` — migrate + server |

### 2.2 Asosiy Kutubxonalar

| Kutubxona | Versiya | Vazifa |
|---|---|---|
| Django | 6.0.3 | Backend framework |
| Django REST Framework | 3.17.1 | REST API endpointlar |
| django-cors-headers | 4.9.0 | Cross-origin so'rovlar |
| django-unfold | 0.87.0 | Zamonaviy Django admin UI |
| Pillow | 12.2.0 | Rasm yuklash va qayta ishlash |
| Faker | 40.12.0 | Test ma'lumotlari |
| Gunicorn | ≥21.2.0 | Production WSGI server |
| psycopg2-binary | ≥2.9.9 | PostgreSQL drayveri |
| dj-database-url | ≥2.1.0 | Database URL konfiguratsiyasi |
| WhiteNoise | ≥6.7.0 | Statik fayllar (production) |
| pandas / numpy | 3.0.2 / 2.4.4 | Dashboard statistika |

### 2.3 Infratuzilma

| Texnologiya | Vazifa |
|---|---|
| Docker | Izolyatsiyalangan muhit |
| Docker Compose | `web` + `db` konteynerlar boshqaruvi |
| PostgreSQL 16 | Production ma'lumotlar bazasi |
| Git + GitHub | Versiya nazorati |

---

## 3. Arxitektura

Loyiha **Django MTV (Model–Template–View)** arxitekturasida qurilgan.

```
Foydalanuvchi (Brauzer)
        |
        | HTTP so'rov
        ↓
   Django URL Router
        |
        ↓
   View (Biznes logika)
    /           \
Model           Template
(PostgreSQL)    (HTML)
                  |
                  ↓ (oddiy so'rov)
             Brauzerga HTML

View → JSON (AJAX so'rov) → Brauzer JS → DOM yangilanadi
```

### AJAX Ishlash Tartibi

```
1. Foydalanuvchi qidiradi yoki filtr tanlaydi
2. 400ms debounce kutiladi (ortiqcha so'rovlar oldini olish)
3. fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
4. Django AJAX ekanini aniqlaydi → faqat qisman HTML qaytaradi
5. JavaScript: container.innerHTML = html
6. history.pushState() — URL yangilanadi, sahifa YANGILANMAYDI
```

---

## 4. Django Ilovalar (Apps) — Batafsil

### 4.1 `apps/accounts` — Foydalanuvchilar Tizimi

**Modeller:**

| Model | Tavsif |
|---|---|
| `CustomUser` | `AbstractUser` asosida. `user_type` (customer/manager), `account_status`, `loyalty_points` |
| `Address` | Yetkazish manzili: shahar, ko'cha, pochta indeksi |
| `SiteSettings` | Singleton — sayt nomi, telefon, ijtimoiy tarmoq linklari |
| `PasswordResetToken` | Parol tiklash uchun vaqtinchalik token |
| `NewsletterSubscriber` | Email obunachilari |

**Asosiy xususiyatlar:**
- Custom foydalanuvchi modeli (email orqali kirish)
- Manager va Customer rollari
- Profil sahifasi (buyurtmalar tarixi, manzillar)

---

### 4.2 `apps/catalog` — Mahsulotlar Katalogi

**Modeller:**

| Model | Tavsif |
|---|---|
| `HeroSection` | Singleton — bosh sahifa hero banneri |
| `Category` | Ierarxik (parent → child). URL slug bo'yicha filtr |
| `Brand` | ASUS, ROG, Lenovo va boshqa brendlar |
| `Product` | Nom, narx, narx_cost, SKU, status, reyting, tavsif |
| `ProductVariant` | Variantlar (xotira, rang) — har birida alohida narx |
| `ProductImage` | Asosiy + qo'shimcha rasmlar |
| `ProductAttribute` | Texnik xususiyatlar (RAM, ekran, protsessor) |
| `Tag` / `ProductTag` | Teglar (#yangi, #aksiya, #top) |
| `Wishlist` | Sevimli mahsulotlar ro'yxati |

**Asosiy xususiyatlar:**
- Kategoriya bo'yicha filtrlash (subcategory qo'llab-quvvatlaydi)
- AJAX qidiruv — debounce bilan
- Reyting va sharh tizimi bilan integratsiya
- Hero banner — admin tomonidan boshqariladi

---

### 4.3 `apps/orders` — Buyurtmalar va Savat

**Modeller:**

| Model | Tavsif |
|---|---|
| `Order` | Buyurtma: raqam, status, to'lov turi, manzil |
| `OrderItem` | Buyurtmadagi har bir mahsulot va miqdori |
| `ShoppingCart` | Sessiya asosidagi vaqtinchalik savat |
| `PaymentTransaction` | To'lov tranzaksiya tarixi |

**Buyurtma statuslari:** `pending → confirmed → shipped → delivered` / `cancelled`

**Asosiy xususiyatlar:**
- AJAX savat (sahifa yangilanmasdan)
- Checkout formasi (yetkazish manzili, to'lov turi)
- Chek chiqarish (print-friendly sahifa)
- Buyurtma holati kuzatuvi

---

### 4.4 `apps/warehouse` — Ombor Boshqaruvi

| Model | Tavsif |
|---|---|
| `Warehouse` | Fizik ombor (nomi, manzili) |
| `Inventory` | Mahsulot zaxirasi (ombor bo'yicha miqdor) |
| `InventoryMovement` | Kirim/chiqim/transfer tarixi |

---

### 4.5 `apps/reviews` — Sharhlar Tizimi

| Model | Tavsif |
|---|---|
| `Review` | 1–5 yulduz baho + matn sharh |
| `ReviewImage` | Sharhga biriktilgan rasmlar (maksimal 5 ta) |

---

### 4.6 `apps/returns` — Qaytarishlar
`Return` va `ReturnItem` — mahsulot qaytarish so'rovlari, sababi va holati.

---

### 4.7 `apps/suppliers` — Yetkazib Beruvchilar
`Supplier`, `PurchaseOrder`, `PurchaseOrderItem` — xarid va ta'minot zanjiri.

---

### 4.8 `apps/manager` — Boshqaruv Paneli

O'zining database modeli yo'q — barcha boshqa app'lar modellarini boshqaradi.

**Sahifalar:**
- Dashboard (statistika: daromad, foyda, buyurtmalar grafigi)
- Buyurtmalar boshqaruvi (AJAX holat o'zgartirish)
- Mahsulot CRUD (Image Cropper bilan)
- Ombor zaxirasi ko'rish
- Foydalanuvchilar ro'yxati va tafsiloti
- Kategoriya va brendlar boshqaruvi
- Storefront sozlamalari (hero banner, sayt nomi)

---

## 5. Sahifalar va URL'lar

### 5.1 Storefront

| # | Sahifa | URL | Template |
|---|---|---|---|
| 1 | Bosh sahifa | `/` | `home.html` |
| 2 | Mahsulotlar katalogi | `/products/` | `catalog/product_list.html` |
| 3 | Kategoriya filtri | `/products/?category=<slug>` | `catalog/product_list.html` |
| 4 | Mahsulot tafsiloti | `/products/<slug>/` | `catalog/product_detail.html` |
| 5 | Savat | `/cart/` | `orders/cart.html` |
| 6 | Checkout | `/checkout/` | `orders/checkout.html` |
| 7 | Buyurtmalar tarixi | `/orders/` | `orders/order_list.html` |
| 8 | Buyurtma tafsiloti | `/orders/<id>/` | `orders/order_detail.html` |
| 9 | Chek chiqarish | `/orders/<id>/receipt/` | `orders/receipt_print.html` |
| 10 | Ro'yxatdan o'tish | `/auth/register/` | `accounts/register.html` |
| 11 | Tizimga kirish | `/auth/login/` | `accounts/login.html` |
| 12 | Profil | `/profile/` | `accounts/profile.html` |
| 13 | Yordam markazi | `/help/` | `catalog/help_page.html` |

### 5.2 Manager Panel

| # | Sahifa | URL |
|---|---|---|
| 14 | Dashboard | `/manager/` |
| 15 | Buyurtmalar | `/manager/orders/` |
| 16 | Buyurtma tafsiloti | `/manager/orders/<id>/` |
| 17 | Mahsulotlar | `/manager/products/` |
| 18 | Mahsulot qo'shish | `/manager/products/add/` |
| 19 | Mahsulot tahrirlash | `/manager/products/<id>/edit/` |
| 20 | Ombor (Zaxira) | `/manager/inventory/` |
| 21 | Foydalanuvchilar | `/manager/users/` |
| 22 | Foydalanuvchi tafsiloti | `/manager/users/<id>/` |
| 23 | Storefront sozlamalari | `/manager/storefront/` |
| 24 | Kategoriyalar | `/manager/categories/` |
| 25 | Brendlar | `/manager/brands/` |

### 5.3 REST API Endpointlar

| Endpoint | Method | Tavsif |
|---|---|---|
| `/api/categories/` | GET | Kategoriyalar ro'yxati |
| `/api/brands/` | GET | Brendlar ro'yxati |
| `/api/products/` | GET | Mahsulotlar (filtr: `?category=`, `?brand=`, `?search=`) |
| `/api/products/<slug>/` | GET | Mahsulot tafsiloti |
| `/api/wishlist/` | GET, POST | Sevimlilar |
| `/api/auth/register/` | POST | Ro'yxatdan o'tish |
| `/api/users/me/` | GET, PUT | Foydalanuvchi profili |
| `/api/addresses/` | GET, POST | Manzillar |
| `/api/orders/` | GET | Buyurtmalar |
| `/api/cart/` | GET | Savat |

> **Jami:** 25 sahifa + 10 API endpoint = **35 ta route**

---

## 6. Fayl Tuzilishi

```
Marketplace/
│
├── 📁 apps/
│   ├── accounts/          # Foydalanuvchilar, auth, profil
│   ├── catalog/           # Mahsulotlar, kategoriyalar, brendlar
│   ├── orders/            # Savat, checkout, buyurtmalar
│   ├── manager/           # ⭐ Boshqaruv paneli
│   ├── warehouse/         # Ombor va zaxira
│   ├── reviews/           # Sharhlar
│   ├── returns/           # Qaytarishlar
│   └── suppliers/         # Yetkazib beruvchilar
│
├── 📁 ecommerce/
│   ├── settings.py        # Django sozlamalari
│   ├── urls.py            # Asosiy URL router
│   ├── wsgi.py            # Production entry point
│   └── dashboard.py       # django-unfold dashboard
│
├── 📁 templates/
│   ├── base.html                    # Asosiy shablon (navbar, footer)
│   ├── home.html                    # Bosh sahifa
│   ├── accounts/                    # Login, Register, Profile
│   ├── catalog/                     # Product list, detail, help
│   ├── orders/                      # Cart, Checkout, Orders, Receipt
│   └── manager/                     # ⭐ Admin sahifalari
│       ├── base_manager.html        # Sidebar + topbar
│       ├── dashboard.html           # Statistika
│       ├── *_list.html              # Ro'yxat sahifalari
│       ├── *_list_partial.html      # AJAX qisman templatelar
│       └── includes/
│           └── image_cropper.html   # Rasm yuklash komponenti
│
├── 📁 static/
│   └── css/style.css      # Global stillar
│
├── 📁 media/              # Yuklangan rasmlar (.gitignore da)
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh          # migrate + collectstatic + gunicorn
├── requirements.txt
└── manage.py
```

---

## 7. Ma'lumotlar Bazasi Sxemasi

```
CustomUser ──< Address
           ──< Order ──< OrderItem >── Product
           ──< ShoppingCart
           ──< Review
           ──< Wishlist

Category ──< Category (parent/child)
         ──< Product ──< ProductVariant
                     ──< ProductImage
                     ──< Inventory >── Warehouse
                                        ──< InventoryMovement

Order ──< PaymentTransaction

Supplier ──< PurchaseOrder ──< PurchaseOrderItem
```

**Jami:** 25+ ta jadval

---

## 8. Dizayn Tizimi

### Storefront (Light Glassmorphism)

| Element | Qiymat |
|---|---|
| Shriftlar | `Outfit` (sarlavha) + `Inter` (matn) |
| Fon | `linear-gradient(135deg, #f5f7fa, #c3cfe2)` |
| Glass karta | `rgba(255,255,255,0.65)` + `backdrop-filter: blur(25px)` |
| Aksent rang | `#006ce1` (ASUS ko'k) |
| Xavf rangi | `#dc2626` |
| Muvaffaqiyat | `#16a34a` |
| Radius | `16px – 28px` |
| Soya | `0 15px 35px rgba(0,0,0,0.05)` |

### Manager Panel (Dark Glassmorphism)

| Element | Qiymat |
|---|---|
| Fon | `#0a0e1a` (to'q ko'k-qora) |
| Glass karta | `rgba(255,255,255,0.04)` + `blur(20px)` |
| Aksent | `#006ce1` |
| Chegara | `rgba(255,255,255,0.08)` |

---

## 9. Ishga Tushirish

### Docker (Production uslubida)

```bash
git clone https://github.com/Shakh07/Marketplace.git
cd Marketplace
docker-compose up --build -d
```

`http://localhost:8000` da ochiladi.

### Lokal (Development)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Foydali buyruqlar

```bash
# Test ma'lumotlarini yuklash
python manage.py seed_data

# Superuser yaratish
python manage.py createsuperuser

# Statik fayllarni yig'ish
python manage.py collectstatic
```

---

## 10. Loyiha Raqamlarda

| Ko'rsatkich | Qiymat |
|---|---|
| Django app'lar | 8 ta |
| Database jadvallar | 25+ ta |
| Veb-sahifalar | 25 ta |
| REST API endpointlar | 10 ta |
| HTML template fayllar | 30+ ta |
| AJAX partial templatelar | 8 ta |
| Python kutubxonalari | 17 ta |
| Dizayn uslubi | ASUS/ROG Glassmorphism |
| Ma'lumotlar bazasi | PostgreSQL 16 |
| Konteynerizatsiya | Docker + Docker Compose |
| Veb-server | Gunicorn (production) |

---

## 👨‍💻 Muallif

**Shohruh** — Loyihani ishlab chiquvchi  
🔗 GitHub: [@Shakh07](https://github.com/Shakh07)  
📁 Repo: [github.com/Shakh07/Marketplace](https://github.com/Shakh07/Marketplace)

---

*NEXUS — kelajak bu yerda.*
