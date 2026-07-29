# 📝 Blog & Social Interaction API (Django REST Framework)

Ushbu loyiha foydalanuvchilarni autentifikatsiya qilish, postlar yaratish, saralash va sahifalash hamda izohlar va layklar tizimini o'z ichiga olgan **RESTful API** loyihasidir. Loyihada tayyor generic/viewset strukturalaridan qochilib, barcha mantiqlar **`APIView`** va **qo'lda yozilgan (manual) biznes mantiqlar** asosida qurilgan.

---

## 🚀 Texnologiyalar Steki

* **Backend Framework:** Python 3.13 / Django 5.x
* **API Framework:** Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JSON Web Token)
* **Database:** SQLite (Development)

---

## 📌 Asosiy Imkoniyatlar va Mantiqlar

### 🔐 Accounts (Foydalanuvchilar)
* **Register:** Yangi foydalanuvchilarni ro'yxatdan o'tkazish.
* **Login & Token Refresh:** JWT access va refresh tokenlarini olish hamda yangilash.
* **Logout:** Refresh tokenni qora ro'yxatga (blacklist) kiritish orqali tizimdan chiqish.
* **Profile & Password Update:** Foydalanuvchi profil ma'lumotlarini ko'rish, tahrirlash va parolni o'zgartirish.

### 📝 Interactions (Postlar)
* **Post CRUD:** Postlarni ko me'yorida yaratish (POST), ko'rish (GET), tahrirlash (PUT) va o'chirish (DELETE).
* **Manual Search & Filter:** Title, Content hamda Author bo'yicha qidirish va filtrlash.
* **Custom Pagination:** Postlar ro'yxatini sahifalab chiqarish.
* **Qo'lda Ruhsatlar Tekshiruvi:** Faqat post muallifigina o'z postini tahrirlashi yoki o'chirishi mumkin.

### 💬 Comments & Likes (Izohlar va Layklar)
* **Izohlar (Comments):**
  * Postga izoh qoldirish va izohlarni ko'rish.
  * Izohni faqat muallifi tahrirlashi mumkin.
  * Izohni izoh muallifi **YOKI** post egasi o'chirish huquqiga ega.
* **Layklar (Likes / Toggle Logic):**
  * **O'z postiga layk taqiqlangan:** Foydalanuvchi o'zi yozgan postga layk bosa olmaydi (400 Bad Request).
  * **Bir marta layk:** Bitta foydalanuvchi bitta postga ko'pi bilan 1 marta layk bosa oladi.
  * **Toggle Mantiqi:** Birinchi marta bosganda layk qo'shiladi, ikkinchi marta bosganda layk olib tashlanadi (Unlike).

---

## 🛠️ O'rnatish va Ishga Tushirish

1. **Repozitoriyadan nusxa olish:**
   ```bash
   git clone <repo-url-link>
   cd blog-1

---

## 🚀 Postman Collection

Loyihadagi barcha API so'rovlarini (Auth, Posts, Comments, Likes) tayyor holatda sinab ko'rish uchun Postman fayli loyiha tarkibiga kiritilgan:

📁 **Postman fayli:** `Blog Site.postman_collection.json`

*(Ushbu faylni Postman dasturiga kirib, **Import** tugmasi orqali yuklab olib ishlatishingiz mumkin)*