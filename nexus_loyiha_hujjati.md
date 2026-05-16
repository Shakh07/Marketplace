# NEXUS — Texnik Hujjat

**Muallif:** Shohruh  
**Loyiha:** [github.com/Shakh07/Marketplace](https://github.com/Shakh07/Marketplace)

---

## Loyiha nima qiladi?

NEXUS — Django asosida yozilgan e-commerce platforma. Xaridor mahsulotlarni ko'rib, savatga qo'shib, buyurtma bera oladi. Operator esa alohida panel orqali buyurtmalarni, mahsulotlarni, ombor zaxirasini va foydalanuvchilarni boshqaradi.

Loyihada ikkita katta qism bor:

- **Storefront** — hamma ko'ra oladigan ochiq qism (bosh sahifa, katalog, savat, profil)
- **Manager Panel** — `/manager/` URL'i orqali kiriladigan yopiq operator paneli

---

## Ilovalar (Django Apps)

Loyiha 8 ta alohida Django ilovasidan tashkil topgan. Har biri o'z vazifasiga javob beradi.

### `accounts` — Foydalanuvchilar

Django'ning standart `AbstractUser` modeli kengaytirilgan. Qo'shimcha maydonlar:

- `user_type` — 3 ta rol: `customer`, `seller`, `admin`
- `account_status` — `active`, `inactive`, `suspended`, `deleted`
- `loyalty_points` — xaridor ball tizimi
- `lifetime_value` — umumiy xaridlar summasi
- `profile_image_url` — profil rasmi

Yaratilgan modellar: `CustomUser`, `Address`, `SiteSettings`, `PasswordResetToken`, `EmailVerificationToken`, `UserSession`, `NewsletterSubscriber`

`SiteSettings` singleton model — ma'muriyat sayt nomini, telefon raqamini, Instagram va Telegram linkini admin paneldan o'zgartira oladi. Doim `pk=1` bo'ladi (har `save()`da `self.pk = 1` qo'yiladi).

---

### `catalog` — Mahsulotlar

Eng ko'p modeli bor ilova.

**`HeroSection`** — bosh sahifaning yuqori qismini (banner) admin boshqaradi. Singleton (`get_or_create(pk=1)`). Sarlavha 3 qatorga bo'lingan, rasm, badge matni va CTA tugma matni bor.

**`Category`** — o'z-o'ziga reference (parent/child). Bir kategoriya boshqa kategoriyaning farzandi bo'lishi mumkin. Slug bo'yicha URL filtrlash ishlaydi.

**`Brand`** — Brend modeli: nom, logo, veb-sayt, kelib chiqqan mamlakat.

**`Product`** — asosiy mahsulot jadvali. Muhim maydonlar:
- `base_price` va `sale_price` — ikkala narx saqlansa, `sale_price` ishlatiladi (`current_price` property)
- `cost_price` — tannarx (manager panelda foyda hisoblash uchun)
- `product_status` — `draft`, `active`, `out_of_stock`, `discontinued`
- `total_stock` — barcha omborlar bo'yicha umumiy zaxira (property, `Sum` agregatsiya)
- `discount_percentage` — chegirma foizi (avtomatik hisoblanadi)

**`ProductVariant`** — mahsulotning variantlari (masalan: 16GB / 32GB). Har birida `price_adjustment` va `stock_quantity` bor.

**`ProductImage`** — asosiy va qo'shimcha rasmlar. `is_primary` maydoni bilan asosiy rasm belgilanadi.

**`ProductAttribute`** — kategoriyaga xos atribut (ekran o'lchami, RAM va h.k.). Turi: text, number, boolean, select, multiselect.

**`Wishlist`** — foydalanuvchi sevimli mahsulotlari. `unique_together` bilan bir mahsulot ikki marta qo'shilmasligi ta'minlangan.

---

### `orders` — Savat va Buyurtmalar

**`Order`** — buyurtma. Holat ketma-ketligi:
```
pending → confirmed → processing → shipped → delivered
                                          ↘ cancelled / refunded
```
Har holat almashtiruvchi vaqt alohida saqlanadi (`confirmed_at`, `shipped_at` va h.k.).

`order_number` saqlanmagan bo'lsa avtomatik UUID asosida hosil qilinadi: `ORD-XXXXXXXX`.

Yetkazish manzili buyurtma vaqtida `Order` ichida saqlanadi (snapshot) — foydalanuvchi keyinchalik manzilini o'zgartirsa, eski buyurtmalar ta'sirlanmaydi.

**`OrderItem`** — buyurtmadagi har bir mahsulot. `save()` da `subtotal = unit_price × quantity` avtomatik hisoblanadi.

**`ShoppingCart`** — foydalanuvchiga tegishli vaqtinchalik savat. `item_total` property orqali qator summasi olinadi.

**`PaymentTransaction`** — to'lov yozuvlari. `recalculate_paid()` metodi barcha `completed` tranzaksiyalar summasini `Order.paid_amount` ga yozadi.

Proxy modellar: `PendingOrder`, `DeliveredOrder` — admin panelda alohida bo'limlar uchun.

---

### `manager` — Operator Paneli

O'zining database jadvali yo'q. Boshqa ilovalarning modellarini o'qib, operator interfeysi ko'rsatadi.

`/manager/` URL prefixsi ostida ishlaydi. Asosiy sahifalar:

| Sahifa | URL |
|---|---|
| Dashboard (statistika) | `/manager/` |
| Buyurtmalar ro'yxati | `/manager/orders/` |
| Buyurtma tafsiloti | `/manager/orders/<id>/` |
| Mahsulotlar | `/manager/products/` |
| Mahsulot qo'shish | `/manager/products/add/` |
| Mahsulot tahrirlash | `/manager/products/<id>/edit/` |
| Ombor zaxirasi | `/manager/inventory/` |
| Foydalanuvchilar | `/manager/users/` |
| Foydalanuvchi tafsiloti | `/manager/users/<id>/` |
| Kategoriyalar | `/manager/categories/` |
| Brendlar | `/manager/brands/` |
| Sayt sozlamalari | `/manager/storefront/` |

AJAX bilan ishlaydi — buyurtma holati, mahsulot qidiruv, jadval filtrlash sahifa yangilanmasdan amalga oshadi. Har bir ro'yxat sahifasining `_partial.html` versiyasi mavjud (faqat jadval qatori qaytaradi).

---

### `warehouse` — Ombor

**`Warehouse`** — fizik ombor (nomi va manzili).  
**`Inventory`** — qaysi mahsulot qaysi ombordan, qancha bor.  
**`InventoryMovement`** — kirim/chiqim/ko'chirish tarixi.

---

### `reviews` — Sharhlar

**`Review`** — 1 dan 5 gacha yulduz baho + matn. Foydalanuvchi faqat xarid qilgan mahsulotga sharh yozishi kerak.  
**`ReviewImage`** — sharhga rasm biriktirish imkoniyati.

---

### `returns` — Qaytarishlar

**`Return`** va **`ReturnItem`** — xaridor mahsulotni qaytarish so'rovi yubora oladi. Holat va sabab saqlanadi.

---

### `suppliers` — Ta'minotchilar

**`Supplier`** — ta'minotchi ma'lumotlari.  
**`PurchaseOrder`** va **`PurchaseOrderItem`** — ta'minotchidan xarid qilish buyurtmasi.

---

## URL Tuzilishi

`ecommerce/urls.py` da barcha ilovalar url'lari birlashtirilgan:

```python
path('admin/', admin.site.urls)        # Django Unfold admin
path('', include('apps.catalog.urls')) # /, /products/, /products/<slug>/
path('', include('apps.accounts.urls'))# /auth/login/, /auth/register/, /profile/
path('', include('apps.orders.urls'))  # /cart/, /checkout/, /orders/
path('manager/', include('apps.manager.urls'))
```

Media fayllar (`/media/`) `re_path` bilan har doim xizmat ko'rsatadi — Gunicorn media fayllarni o'zi serve qilmagani uchun.

---

## Django Sozlamalari (`settings.py`)

Muhim nuqtalar:

- `AUTH_USER_MODEL = 'accounts.CustomUser'` — custom user model
- Vaqt zonasi: `Asia/Tashkent`
- Son formati: bo'sh joy bilan guruhlash (`1 000 000`)
- `STATICFILES_STORAGE` — WhiteNoise kompressiya + cache-busting
- Ma'lumotlar bazasi: `DATABASE_URL` muhit o'zgaruvchisi bo'lsa — u ishlatiladi, yo'q bo'lsa alohida `DB_*` o'zgaruvchilar
- `DEBUG=False` bo'lganda HTTPS sozlamalari avtomatik yoqiladi (HSTS, SSL redirect va h.k.)
- CORS: production'da `CORS_ALLOWED_ORIGINS`, local'da hamma manbaga ruxsat

`django-unfold` admin paneli NEXUS ko'k rangi (`0 108 225`) bilan sozlangan. Sidebar'da BOSHQARUV, KATALOG, SOTUVLAR, FOYDALANUVCHILAR, SOZLAMALAR bo'limlari bor.

---

## Dizayn

Ikkita alohida tema bor:

**Storefront (açiq, kunduzgi):**
- Fon: gradient `#f5f7fa → #c3cfe2`
- Kartalar: `rgba(255,255,255,0.65)` + `blur(25px)`
- Aksent rang: `#006ce1`

**Manager Panel (qorong'u):**
- Fon: `#0a0e1a`
- Kartalar: `rgba(255,255,255,0.04)` + `blur(20px)`
- Chegara: `rgba(255,255,255,0.08)`

Har ikkisida ham `Inter` va `Outfit` shriftlari ishlatilgan.

---

## Raqamlarda

| Ko'rsatkich | Qiymat |
|---|---|
| Django ilovalar | 8 |
| Database jadvallari | 28+ |
| HTML template fayllar | 30+ |
| AJAX partial templatelar | 8 |
| Operator panel sahifalari | 12 |
| Storefront sahifalari | 13 |
| Python kutubxonalari | 17 |

---

*Muallif: Shohruh · 2026*
