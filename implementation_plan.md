# Nasiya (Qarzga Tovar Berish) Tizimini Yaratish

Foydalanuvchining talabidan men quyidagilarni tushundim:
Sizga nafaqat odatiy mijozlarga, balki **boshqa do'konchilar, tanishlar yoki ulgurji xaridorlarga qarzga (nasiyaga) tovar berishni boshqaradigan alohida bo'lim** kerak. Bu tizimda:
- Kimga qancha miqdorda tovar berilgani,
- Jami qarz summasi va oldindan to'langan qismi,
- Qarzni qaytarish muddati (shartnoma vaqti),
- Qarz qachon va qancha miqdorda (qismlarga bo'lib) qaytarilgani tarixi,
- Va ularni qulay tarzda boshqarish, monitoring qilish (muddatidan o'tgan qarzlarni qizil bilan ko'rsatish) imkoniyati bo'lishi kerak.

## Yechim va Takliflarim (Proposals)

Bizda allaqachon ajoyib ishlayotgan **Buyurtmalar (Orders)** va **To'lovlar (PaymentTransaction)** tizimi mavjud. Shularni noldan qayta yozmasdan, eng optimal yo'l — `Order` modelini biroz kengaytirib, maxsus **"Nasiyalar (Credits)" bo'limini** yaratishdir.

### 1. Modelni Kengaytirish (Database Changes)
`Order` modeliga quyidagi maydonlarni qo'shamiz:
- `order_type`: Buyurtma turini belgilaydi (Masalan: `retail` - oddiy chakana savdo, `credit` - nasiya savdo).
- `due_date`: Qarzni qaytarishning so'nggi muddati (qachongacha pulni berishi kerak).
- `client_type` / B2B ma'lumotlari: Do'kon nomi yoki shaxs turi.

*Izoh: Nasiyalar ham aslini olganda "Buyurtma", shuning uchun inventar (Ombor/Zaxira)dan tovar avtomatik yechilishi, qismlab to'lash tizimi hozirgi mavjud kodlarga juda mos tushadi.*

### 2. Menejer Panelida "Nasiyalar" Alohida Bo'limi
Admin menyusiga **"Nasiyalar (Qarzlar)"** degan yangi menyu qo'shamiz (`/manager/credits/`).
- **Ro'yxat (List View):** Bu yerda faqat `order_type='credit'` bo'lganlar ko'rinadi. Ro'yxatda jami qarz, to'langan qismi, **qoldiq qarz** va **qaytarish muddati** alohida ustunlarda bo'ladi. Muddati yaqinlashgan yoki o'tib ketgan nasiyalar avtomatik qizil rangda ogohlantirib turadi.
- **Yangi Nasiya Yaratish:** Menejer o'zi qo'lda mijoz ismi, olgan tovarlari ro'yxati va qaytarish muddatini kiritib formani saqlaydi.

### 3. Nasiya Tafsilotlari (Detail View)
- Bugun biz qanday qilib to'lovlarni qism-qism qilib qo'shishni va "To'lov tarixi"ni ko'rsatishni qildik, xuddi shu narsa nasiyada ham ishlaydi. 
- Qarz summasi har safar mijoz ozgina pul olib kelganda `+ Qo'shish` orqali kiritilib boriladi.
- Dastur qachon qancha to'langanini va umumiy qarzdan qancha qolganini avtomatik hisoblab, nolga yetganda statusni "To'langan (Yopilgan)" deb o'zgartiradi.

## User Review Required

> [!IMPORTANT]
> Iltimos, quyidagilarga o'z fikringizni bildiring:
> 1. **Mijozlar bazasi:** Nasiya beriladigan odamlar (yoki do'konlar) tizimda oddiy User (xaridor) sifatida saqlanib, ularning profilida jami nasiyalari ko'rinib tursinmi yoki ular uchun alohida e-commerce'dan tashqari faqat ism/telefon yoziladigan oddiy mijoz/do'kon modeli yarataylikmi? 
> 2. Oddiy e-commerce buyurtmalari bilan inventarizatsiya (zaxira) bitta joydan yechilishi (ya'ni omborda 10 ta telefon bo'lsa, kimdir saytdan sotib olsa ham, siz nasiyaga birovga bersangiz ham bir xil ombordan kamayishi) to'g'rimi? 

Agar ushbu reja (Implementation plan) ma'qul kelsa, tasdiqlang va men buni amalga oshirishni boshlayman.
