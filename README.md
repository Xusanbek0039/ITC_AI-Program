# ITC_AI-Program

# 🚀 AI Chat App (Django DRF + OpenAI + Python APK)

> 🔥 Zamonaviy AI chat ilova: Django backend + OpenAI + Python (Kivy) mobil APK
> 💡 IT Creative tomonidan ishlab chiqilgan

---

## 📌 Loyiha haqida

Bu loyiha — **OpenAI asosida ishlovchi chat ilova** bo‘lib, quyidagi texnologiyalar asosida qurilgan:

* 🧠 AI: OpenAI API
* ⚙️ Backend: Django + Django REST Framework
* 📱 Mobile: Python (Kivy / KivyMD)
* 🗄️ Database: PostgreSQL
* 🔐 Auth: JWT Token Authentication

Foydalanuvchilar:

* Chat orqali AI bilan suhbatlashadi
* Har bir user uchun alohida chat history saqlanadi
* Chat sessionlar orqali ishlaydi

---

## 🧱 Arxitektura

```
[ Mobile APK (Kivy) ]
            ↓
        REST API
            ↓
[ Django DRF Backend ]
            ↓
[ OpenAI API ]
```

### 🔑 Muhim:

* ❌ OpenAI API key mobil ilovada YO‘Q
* ✅ API key faqat backend (.env) ichida
* 🔐 Backend OpenAI bilan vositachi

---

## ✨ Asosiy imkoniyatlar

* 🔐 Register / Login (JWT)
* 💬 AI Chat (OpenAI orqali)
* 📚 Chat history saqlash
* 🧵 Chat sessionlar
* 📄 Eski chatlarni ko‘rish
* 🧠 AI javoblar (context bilan)
* ⚡ Tezkor API response
* 🛡️ Secure architecture

---

## 🗂️ Loyiha tuzilmasi

```
backend/
│
├── apps/
│   ├── users/
│   ├── chat/
│   ├── openai_service/
│   ├── common/
│   └── billing/ (future)
│
├── config/
├── manage.py
└── requirements.txt

mobile_app/
├── main.py
├── screens/
├── services/
└── components/
```

---

## 🗄️ Database modellari

### 👤 User

* username
* email
* password

### 💬 ChatSession

* user (FK)
* title
* created_at

### 📨 ChatMessage

* session (FK)
* role (user / assistant)
* content
* created_at

### 📊 UsageLog

* user
* tokens_used
* created_at

---

## 🔌 API Endpointlar

### 🔐 Auth

```
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/refresh/
GET    /api/profile/
```

### 💬 Chat

```
POST   /api/chat/create/
GET    /api/chat/list/
GET    /api/chat/<id>/
DELETE /api/chat/<id>/
```

### 📨 Messages

```
GET    /api/messages/<chat_id>/
POST   /api/messages/send/
```

---

## 🧠 OpenAI Integration

* Backend orqali ishlaydi
* Service layer orqali chaqiriladi
* Chat history context sifatida yuboriladi

### 🔥 Flow:

```
User message → Django → OpenAI → Response → DB → Mobile
```

---

## 🔐 Xavfsizlik

* 🔑 API key faqat `.env` ichida
* 🔐 JWT authentication
* 🚫 Rate limiting
* 🛡️ Input validation
* 🌐 HTTPS
* 🔒 CORS himoya

---

## 📱 Mobile ilova (Kivy)

### Screenlar:

* Login Screen
* Register Screen
* Chat List
* Chat Detail
* Profile

### Flow:

```
Login → Chat List → Chat → AI Response
```

---

## ⚙️ O‘rnatish (Backend)

```bash
git clone https://github.com/your-repo/ai-chat-app.git
cd ai-chat-app/backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔑 .env sozlash

```env
SECRET_KEY=your_secret_key
DEBUG=True

OPENAI_API_KEY=your_openai_key

DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

---

## ▶️ Run qilish

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📱 APK build qilish

```bash
buildozer init
buildozer android debug
```

> ⚠️ Tavsiya: Linux yoki WSL ishlating

---

## 🧪 Testlar

```bash
python manage.py test
```

---

## 🚀 Deployment

* Gunicorn
* Nginx
* PostgreSQL
* SSL (HTTPS)

---

## 🔮 Kelajak rejalari

* 🎤 Voice chat
* 🖼️ Image input
* 📁 File upload
* 💳 Subscription system
* 📊 Admin analytics
* 🤖 Multi-model support

---

## 🧑‍💻 Muallif

**Husan Suyunov**
💻 IT Creative
📺 YouTube: IT Creative

---

## ⭐ Qo‘llab-quvvatlash

Agar loyiha sizga yoqsa:

* ⭐ Star bosing
* 🔁 Ulashing
* 💬 Feedback qoldiring

---

## ⚡ Qisqa xulosa

Bu loyiha:

* 🔥 Zamonaviy AI chat app
* 🧠 OpenAI integratsiya
* ⚙️ Django DRF backend
* 📱 Python APK ilova

---

💡 **"O‘yin o‘ynamang — o‘yinni o‘zingiz yarating!"**
