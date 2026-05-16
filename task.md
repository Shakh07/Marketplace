# Nasiya (Credit Sales) Implementation Task List

- `[x]` 1. **Modelni yangilash:**
  - `[x]` `Order` modeliga `order_type` (chakana, nasiya) va `due_date` maydonlarini qo'shish.
  - `[x]` Makemigrations va migrate bajarish.

- `[x]` 2. **Menyu va Yo'riqnoma (Routing):**
  - `[x]` `base_manager.html` saydebarida "Nasiyalar" bo'limi qo'shish.
  - `[x]` `apps/manager/urls.py` ga nasiya ro'yxati va yaratish sahifalari yo'nalishlarini (routes) qo'shish.

- `[x]` 3. **Nasiya Yaratish (Create Credit):**
  - `[x]` Admin tomonidan nasiya qo'shish uchun view yozish (`manager_credit_create`). Mijoz ism/telefon, qarz muddati va mahsulotlarni tanlash.
  - `[x]` Dastlabki to'lov kiritish (agar mavjud bo'lsa) logikasini qo'shish.
  - `[x]` Zaxira (Inventory) dan mahsulotlarni ayirib tashlash mantiqini sozlash.
  - `[x]` `credit_form.html` shablonini frontendda chiroyli qilib UI yaratish (JS orqali qator-qator mahsulot qo'shish).

- `[x]` 4. **Nasiyalar Ro'yxati (List View):**
  - `[x]` `credit_list.html` sahifasini yaratish (muddatidan o'tgan qarzlarni qizil rangda ajratib ko'rsatish).
  
- `[x]` 5. **Nasiya Tafsilotlari (Detail View):**
  - `[x]` Nasiya tafsilotlarini mavjud `order_detail` da moslashtirib chiqarish (`order_type` ga qarab).
  - `[x]` To'lov tarixini sinovdan o'tkazish.

- `[x]` 6. **Tekshirish:**
  - `[x]` Barcha jarayonlarni qadam-baqadam tekshirish (qarz nolga tushganda status yopilishi va boshqalar).
