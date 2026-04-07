# ITC_AI-Program

Sen senior software architect va senior full stack mobile/backend developersan.

Menga quyidagi loyiha uchun PROFESSIONAL, PRODUCTION-READY arxitektura, papkalar tuzilmasi, texnologiyalar tanlovi, API flow va xavfsizlik yondashuvini to‘liq ishlab ber:

LOYIHA NOMI:
OpenAI asosidagi chat ilova

ASOSIY MAQSAD:
Men Django DRF orqali backend API yozmoqchiman.
Mobil tomoni Python orqali yoziladi va Android APK ko‘rinishida ishlaydi.
Ilovada foydalanuvchi chat oynasida savol yuboradi, backend esa OpenAI API orqali javob olib qaytaradi.

MUHIM TALABLAR:
1. OpenAI API key hech qachon APK ichida bo‘lmasin.
2. API key faqat Django serverdagi .env faylda saqlansin.
3. Mobil ilova faqat mening Django API serverimga murojaat qilsin.
4. Django backend OpenAI bilan vositachi bo‘lib ishlasin.
5. Chat history bazada saqlansin.
6. Har bir userning alohida suhbatlari bo‘lsin.
7. Login / register / token auth bo‘lsin.
8. Chat sessiyalar bo‘yicha ishlasin.
9. Yangi chat ochish, eski chatlar ro‘yxati, bitta chat ichidagi xabarlarni ko‘rish bo‘lsin.
10. Foydalanuvchi xabari va AI javobi alohida message modelda saqlansin.
11. Streaming bo‘lsa bonus, bo‘lmasa oddiy response ham mayli.
12. Error handling, timeout, retry, rate limit, logging va basic security bo‘lsin.
13. Kelajakda subscription yoki token-limit qo‘shish mumkin bo‘ladigan arxitektura bo‘lsin.
14. Kodlar clean architecture tamoyiliga yaqin bo‘lsin.
15. Backend kengayadigan bo‘lsin: chatbot, file upload, voice, admin panel, analytics keyin qo‘shish oson bo‘lsin.

MENGA QUYIDAGILARNI CHIQARIB BER:

1. UMUMIY ARXITEKTURA
- system design
- client-server flow
- Django DRF + OpenAI + Python APK app o‘rtasidagi aloqa sxemasi
- request/response jarayoni
- authentication flow
- chat session flow
- message persistence flow

2. TEXNOLOGIYALAR TANLOVI
- Backend uchun: Django, Django DRF, PostgreSQL, Redis kerakmi yo‘qmi, Celery kerakmi yo‘qmi
- Mobile uchun: Python asosida Kivy yoki KivyMD eng mos variantini tanla va nima uchun tanlaganingni tushuntir
- Deployment uchun tavsiya: Nginx + Gunicorn + PostgreSQL
- Environment config va secrets management

3. PAPKALAR TUZILMASI
Professional loyiha structure yoz:
- backend/
- apps/users/
- apps/chat/
- apps/openai_service/
- apps/billing/ (future)
- apps/common/
- config/
- requirements/
- mobile_app/
- services/
- repositories/
- serializers/
- urls/
- tests/

4. DATABASE MODELLAR
Quyidagi modellarga aniq tavsif ber:
- User
- ChatSession
- ChatMessage
- AIModelConfig
- UsageLog
- SubscriptionPlan (future)
- UserQuota (future)

Har bir model uchun:
- fieldlar
- field type
- relations
- nima uchun kerakligi

5. API ENDPOINTLAR
REST API endpointlar yozib ber:
- register
- login
- refresh token
- profile
- create new chat
- list chats
- chat detail
- list messages
- send message
- rename chat
- delete chat
- usage stats
- optional: stream response endpoint

Har biri uchun:
- method
- url
- request body
- response body
- auth kerak yoki yo‘q
- sample JSON

6. OPENAI INTEGRATION QISMI
- Django ichida OpenAI service layer qanday yoziladi
- view ichida to‘g‘ridan-to‘g‘ri chaqirmasdan service class ishlat
- OpenAI API ga request yuborish flow
- system prompt, user prompt, history qanday yig‘iladi
- token limitni qanday nazorat qilish mumkin
- xatolik chiqsa qanday fallback ishlaydi
- timeout va retry qayerda bo‘ladi
- model tanlash qanday qilinadi

7. XAVFSIZLIK
Juda muhim:
- Nega API key APK ichida bo‘lmasligi kerak
- Backend proxy pattern tushuntir
- JWT auth yoki session authdan qaysi biri mobil ilova uchun yaxshi
- rate limiting
- abuse prevention
- input validation
- logging
- CORS
- HTTPS
- .env ishlatish
- admin access himoyasi

8. MOBILE APP ARXITEKTURASI
Python bilan yoziladigan APK uchun:
- screenlar ro‘yxati
- navigation flow
- login screen
- register screen
- chat list screen
- chat detail screen
- settings/profile screen
- local storage
- token saqlash
- API client class
- loading, error, empty state
- UI state management
- MVC/MVVMga yaqin sodda arxitektura tavsiya qil

9. BOSQICHMA-BOSQICH ISH REJA
MVP dan productiongacha step-by-step plan yoz:
1-bosqich backend auth
2-bosqich chat models
3-bosqich OpenAI integration
4-bosqich mobile UI
5-bosqich chat history
6-bosqich testing
7-bosqich deploy
8-bosqich optimization

10. KOD YOZISH STILI
- clean code
- reusable service
- serializer alohida
- business logic service layer’da
- constants/config alohida
- exception handling alohida
- response format bir xil bo‘lsin

11. NAMUNAVIY KODLAR
Quyidagilar uchun minimal namunaviy kod yozib ber:
- Django modellar
- serializerlar
- DRF viewlar
- OpenAI service class
- urls.py
- .env example
- settings.py config
- mobile app API service class
- mobile app chat request yuborish misoli

12. TESTLAR
- backend unit test
- API test
- auth test
- chat creation test
- message send test
- OpenAI service mock test

13. DEPLOYMENT
- production deployment architecture
- domain + SSL
- static/media
- gunicorn
- nginx
- postgres
- environment variables
- logging va monitoring

14. FUTURE FEATURES
- voice chat
- image input
- file upload
- teacher/student mode
- multi-model support
- admin analytics
- token billing
- offline cache

FORMAT:
Javobni juda tartibli qil.
Avval high-level architecture ber.
Keyin componentlar.
Keyin folder structure.
Keyin models.
Keyin endpoints.
Keyin security.
Keyin mobile structure.
Keyin roadmap.
Keyin kod skeleton.

Javobda real production tavsiyalar ber.
Faqat nazariya emas, amaliy yondashuv bo‘lsin.
Kerak joylarda diagramma ko‘rinishida ASCII architecture ham yoz.
Har bo‘limda “nima uchun aynan shu yechim tanlandi” degan izoh ber.