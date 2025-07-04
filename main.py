from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import smtplib
import random
import hashlib
import shutil
import os
from email.mime.text import MIMEText

app = FastAPI()
# app.mount("/videos", StaticFiles(directory="videos"), name="videos")

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}

# Statik fayllar uchun papkalarni yaratish
os.makedirs("avatars", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# Statik fayllarni ulash
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email sozlamalari
SENDER_EMAIL = "muham20021202@gmail.com"
APP_PASSWORD = "kxnx qmzg qtbc guhm"
ADMIN_EMAIL = "muham20021202@gmail.com"

# ---- MODELLAR ----

class Lesson(BaseModel):
    id: int
    category: Dict[str, str]
    title: Optional[Dict[str, str]] = None
    description: Dict[str, str]
    subtitle: Dict[str, str]
    answer: Dict[str, str]
    video_url: Optional[str] = None  

class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class VerifyInput(BaseModel):
    code: str   

class Comment(BaseModel):
    name: Optional[str] = None
    email: str
    message: str

class UserOutput(BaseModel):
    email: str
    image: str
    name: Optional[str] = None

# ---- MA'LUMOTLAR OMBORI ----

lessons = [
    {
        "id": 1,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Word kirish va sozlamalar",
            "rus": "Введение в Word и настройки",
            "eng": "Introduction to Word and settings"
        },
        "description": {
            "uz": "Word dasturiga kirish va sozlamalar",
            "rus": "Введение в программу Word и настройки",
            "eng": "Introduction to Word and settings"
        },
        "subtitle": {
            "uz": "Word nima uchun kerak?",
            "rus": "Зачем нужен Word?",
            "eng": "Why is Word needed?"
        },
        "answer": {
            "uz": "Microsoft Word matn yaratish, tahrirlash va formatlash uchun kerak",
            "rus": "Microsoft Word нужен для создания, редактирования и форматирования текста",
            "eng": "Microsoft Word is used to create, edit, and format text"
        },
       
"video_url": " https://drive.google.com/file/d/1xF1lYv-jG3Ibo1z2ksKDgmXowUIOc56V/preview"

    },
  {
        "id": 2,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Vstavka bo'limini to'liq o'rganish",
            "rus": "Полное изучение раздела вставки",
            "eng": "Complete study of the Insert section"
        },
        "description": {
            "uz": "Vstavka bo'limi haqida",
            "rus": "О разделе «Вставка»",
            "eng": "About the Insert section"
        },
        "subtitle": {
            "uz": "Vstavka bo'limida nimalar o'rganamiz?",
            "rus": "Что мы узнаем во вставке?",
            "eng": "What will we learn in the Insert section?"
        },
        "answer": {
            "uz": "“Vstavka” bo‘limida hujjatga rasm, jadval, diagramma, shakl, matn qutisi, sahifa raqami, sarlavha, formulalar va havolalar qo‘shishni o‘rganamiz. Bu bo‘lim hujjatni chiroyli va tushunarli qilishga yordam beradi.",
            "rus": "В разделе «Вставка» мы узнаем, как добавлять в документ изображения, таблицы, диаграммы, фигуры, текстовые поля, номера страниц, заголовки, формулы и ссылки. Этот раздел поможет сделать документ красивым и понятным.",
            "eng": "In the 'Insert' section, we will learn how to add images, tables, charts, shapes, text boxes, page numbers, headings, formulas, and links to a document. This section will help you make your document beautiful and understandable."
        },
             "video_url": "https://drive.google.com/file/d/1zcA_MvsLv9tgWgFxDymmYksIOeArSCH5/preview"

    },
    {
        "id": 3,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Maket Dizayn bo'limlari xaqida",
            "rus": "Работа с таблицами в разделе «Вставка»",
            "eng": "Working with Tables in the Insert section"
        },
        "description": {
            "uz": "Maket Dizayn bo'limlari bilan ishlash",
            "rus": "Полная работа с вкладками.",
            "eng": "Full work with tabs."
        },
        "subtitle": {
            "uz": "Bizga Maket Dizayn bo'limlari nima uchun kerak?",
            "rus": "Зачем нам нужны Таблицы?",
            "eng": "Why do we need Tables?"
        },
        "answer": {
            "uz": "Tablitsiyalar — matnda so‘zlarni aniq joylashtirish uchun kerak. Ular yordamida matnni chiziqlar bo‘yicha to‘g‘ri tartibda joylashtirish osonlashadi. Masalan, jadval yasashda yoki ro‘yxatlarni tartibga solishda foydali.",
            "rus": "Таблицы необходимы для точного расположения слов в тексте. Они облегчают размещение текста в правильном порядке вдоль строк. Например, это полезно для создания таблиц или организации списков.",
            "eng": "Tables are used to precisely position words in text. They make it easier to arrange text in the correct order on lines. For example, they are useful when creating tables or organizing lists."
        },
        "video_url": "https://drive.google.com/file/d/1ycDTPAHXP1TzVy4IJcnjJk9xHuLKo1VB/preview"
    },
    {
        "id": 4,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Dizayn, Maket va Vid bo'limlari",
            "rus": "Отделы Дизайн, Макет и Вид",
            "eng": "Design, Layout, and View Departments"
        },
        "description": {
            "uz": "Dizayn, Maket va Vid bo'limlari bilan ishlash",
            "rus": "Работа с разделами Дизайн, Макет и Вид",
            "eng": "Working with the Design, Layout, and View tabs"
        },
        "subtitle": {
            "uz": "Dizayn, Maket va Vid bo'limlari nima uchun kerak?",
            "rus": "Зачем нужны разделы Дизайн, Макет и Вид?",
            "eng": "Why are the Design, Layout, and View sections needed?"
        },
        "answer": {
            "uz": "Dizayn bo‘limi: Hujjatga fon, rang, chegara (border) va mavzu (theme) qo‘shish uchun. Maket bo‘limi: Sahifa o‘lchami, chekkalar (margin), yo‘nalish (orientation) va ustunlarni sozlash uchun. Vid (View) bo‘limi: Hujjatni ko‘rish usullarini o‘zgartirish (masalan: bosma ko‘rinish, web ko‘rinish) va panjaralar, liniyalar ko‘rsatish yoki yashirish uchun.",
            "rus": "Вкладка 'Дизайн' – используется для добавления фона, цвета, рамки и темы в документ. Вкладка 'Разметка страницы' (или 'Макет') – используется для настройки размера страницы, полей, ориентации и колонок. Вкладка 'Вид' – используется для изменения способа отображения документа (например: разметка страницы, веб-документ) и для показа или скрытия сетки и линеек.",
            "eng": "Design tab: Used to add background, color, borders, and themes to the document. Layout tab: Used to set page size, margins, orientation, and columns. View tab: Used to change how the document is displayed (e.g., Print Layout, Web Layout) and to show or hide gridlines and rulers."
        },
        "video_url": "https://www.youtube.com/embed/FSomOOePKWQ?si=tbtpUnOe5iqLa7bp&rel=0&modestbranding=1&iv_load_policy=3&controls=1&loop=0"
    },
    {
        "id": 5,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Havolalar bilan ishlash",
            "rus": "Работа со ссылками",
            "eng": "Working with links"
        },
        "description": {
            "uz": "Ichki va tashqi havolalar",
            "rus": "Внутренние и внешние ссылки",
            "eng": "Internal and External Links"
        },
        "subtitle": {
            "uz": "Havolalar nima uchun kerak?",
            "rus": "Зачем нужны ссылки?",
            "eng": "Why are links needed?"
        },
        "answer": {
            "uz": "Boshqa hujjatlarga, veb-saytlarga yoki hujjat ichidagi joylarga tez va oson o'tishni ta'minlaydi. Matnni interaktiv qiladi. Ma'lumotlarni bog'lash va izlashni osonlashtiradi.",
            "rus": "Обеспечивает быстрый и лёгкий переход к другим документам, веб-сайтам или местам внутри документа. Делает текст интерактивным. Упрощает связывание и поиск информации.",
            "eng": "Enables quick and easy navigation to other documents, websites, or places within the document. Makes the text interactive. Simplifies linking and searching for information."
        },
        "video_url": "https://www.youtube.com/embed/06iFWXxXowM?si=LctlpzOvwskWjIp-&rel=0&modestbranding=1&iv_load_policy=3&controls=1&loop=0"
    },
    {
        "id": 7,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
        },
        "title": {
            "uz": "Xavfsizlikka e'tibor berish",
            "rus": "Сосредоточьтесь на безопасности",
            "eng": "Focus on safety"
        },
        "description": {
            "uz": "Xavfsizlik. Hujjatlarni tahrirlashdan himoyalash. Saqlanmagan hujjatlarni tiklash",
            "rus": "Безопасность. Защитите документы от редактирования. Восстановить несохраненные документы",
            "eng": "Security. Protect documents from editing. Recover unsaved documents"
        },
        "subtitle": {
            "uz": "Word da hujjatlarni himoyalash nima uchun kerak?",
            "rus": "Почему необходимо защищать документы в Word?",
            "eng": "Why is it necessary to protect documents in Word?"
        },
        "answer": {
            "uz": "Hujjatni o‘zgartirishdan yoki o‘chirishdan, maxfiy yoki muhim ma’lumotlarni himoya qilish va foydalanuvchilar faqat o‘qish uchun hujjatni ko‘rishlari mumkin bo‘lishi uchun kerak.",
            "rus": "Защита документа от изменений или удаления, сохранение конфиденциальной или важной информации и предоставление пользователям возможности просматривать документ только в режиме чтения.",
            "eng": "Protecting the document from changes or deletion, safeguarding confidential or important information, and allowing users to view the document in read-only mode."
        },
        "video_url": "https://www.youtube.com/embed/TtD9rpinYiQ?si=L_iWsEdBwKt4osVt&rel=0&modestbranding=1&iv_load_policy=3&controls=1&loop=0"
    },
    {
        "id": 8,
        "category": {
            "uz": "Excel darslari",
            "rus": "Уроки Excel",
            "eng": "Excel lessons"
        },
        "description": {
            "uz": "Excel dasturi va interfeysi",
            "rus": "Программа и интерфейс Excel",
            "eng": "Excel program and interface"
        },
        "subtitle": {
            "uz": "Excel dasturi nima uchun kerak?",
            "rus": "Зачем нужна программа Excel?",
            "eng": "Why is the Excel program needed?"
        },
        "answer": {
            "uz": "Bu jadval ko‘rinishida ma’lumotlarni kiritish, tartiblash, tahlil qilish va hisob-kitoblar qilish uchun mo‘ljallangan dasturdir.",
            "rus": "Это программа, предназначенная для ввода, сортировки, анализа данных и выполнения расчетов в табличной форме.",
            "eng": "It is a program designed for entering, sorting, analyzing data, and performing calculations in a tabular format."
        },
        "video_url": "https://www.youtube.com/embed/K60jl2ZRAz0?si=-Dw43bBxHnoSDKXm&rel=0&modestbranding=1&iv_load_policy=3&controls=1&loop=0"
    },
    {
        "id": 9,
        "category": {
            "uz": "Excel darslari",
            "rus": "Уроки Excel",
            "eng": "Excel lessons"
        },
        "description": {
            "uz": "Excel dasturida Smart Jadval yaratish",
            "rus": "Создание умной таблицы в программе Excel",
            "eng": "Creating a smart table in Excel"
        },
        "subtitle": {
            "uz": "Excel dasturida jadvallar bilan qanday ishlaymiz?",
            "rus": "Как работать с таблицами в Excel?",
            "eng": "How do we work with tables in Excel?"
        },
        "answer": {
            "uz": "Excel’da jadvallar bilan ishlashda ma’lumotlar kiritiladi, tartiblanadi, filtrlanadi, formulalar yordamida hisob-kitob qilinadi va grafiklar orqali tahlil qilinadi.",
            "rus": "В Excel при работе с таблицами данные вводятся, сортируются, фильтруются, производятся вычисления с помощью формул и анализируются с помощью диаграмм.",
            "eng": "In Excel, when working with tables, data is entered, sorted, filtered, calculated using formulas, and analyzed using charts."
        },
        "video_url": "https://www.youtube.com/embed/iCVfDVEh-80?si=KrXXicJJYujyR_Ia&rel=0&modestbranding=1&iv_load_policy=3&controls=1&loop=0"
    }
]

TEMP_USERS: Dict[str, dict] = {}
USERS: List[Dict[str, str]] = []
comments: Dict[int, List[Comment]] = {}

# ---- API YO‘LLARI ----

@app.get("/lessons", response_model=List[Lesson])
def get_lessons(lang: Optional[str] = Query("uz")):
    result = []
    for lesson in lessons:
        result.append(Lesson(
            id=lesson["id"],
            category={lang: lesson["category"].get(lang, lesson["category"]["uz"])},
            title={lang: lesson["title"].get(lang, lesson.get("title", {}).get("uz"))} if lesson.get("title") else None,
            description={lang: lesson["description"].get(lang, lesson["description"]["uz"])},
            subtitle={lang: lesson["subtitle"].get(lang, lesson["subtitle"]["uz"])},
            answer={lang: lesson["answer"].get(lang, lesson["answer"]["uz"])},
            video_url=lesson.get("video_url")
        ))
    return result

@app.get("/lessons/{lesson_id}", response_model=Lesson)
def get_lesson_by_id(lesson_id: int):
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            return Lesson(**lesson)
    raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")

@app.post("/register")
def register(user: RegisterInput):
    if user.email in TEMP_USERS:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan.")
    verify_code = str(random.randint(100000, 999999))
    TEMP_USERS[user.email] = {
        "password": user.password,
        "code": verify_code,
        "name": user.name
    }
    msg = MIMEText(f"Sizning tasdiqlash kodingiz: {verify_code}")
    msg["Subject"] = "Tasdiqlash kodi"
    msg["From"] = SENDER_EMAIL
    msg["To"] = user.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    return {"message": "Kod yuborildi"}

@app.post("/verify")
def verify_code(data: VerifyInput):
    for email, user_data in TEMP_USERS.items():
        if user_data["code"] == data.code:
            email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
            image_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
            USERS.append({
                "email": email,
                "password": user_data["password"],
                "image": image_url,
                "name": user_data.get("name")
            })
            del TEMP_USERS[email]
            return {"message": "Tasdiqlandi va ro'yxatdan o'tdingiz", "image": image_url}
    raise HTTPException(status_code=400, detail="Kod noto‘g‘ri")

@app.post("/upload-avatar")
async def upload_avatar(email: str = Form(...), image: UploadFile = File(...)):
    filename = f"avatars/{email.replace('@', '_')}.png"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    file_url = f"https://backend-s1qc.onrender.com/avatars/{email.replace('@', '_')}.png"
    return {"message": "Rasm saqlandi", "image": file_url}

@app.post("/lessons/{lesson_id}/comments")
def add_comment(lesson_id: int, comment: Comment):
    lesson_ids = [lesson["id"] for lesson in lessons]
    if lesson_id not in lesson_ids:
        raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")

    if lesson_id not in comments:
        comments[lesson_id] = []
    comments[lesson_id].append(comment)

    comment_name = comment.name or "Ism ko'rsatilmagan"

    # Admin email
    admin_body = f"""🔔 Yangi izoh keldi!

🆔 Dars ID: {lesson_id}
👤 Ism: {comment_name}
📧 Email: {comment.email}

💬 Xabar:
{comment.message}
"""
    admin_msg = MIMEText(admin_body)
    admin_msg["Subject"] = f"Dars {lesson_id} uchun yangi izoh"
    admin_msg["From"] = SENDER_EMAIL
    admin_msg["To"] = ADMIN_EMAIL
    admin_msg["Reply-To"] = comment.email

    # User email
    user_body = f"""Salom {comment_name},

Izohingiz uchun rahmat! Tez orada sizga javob beramiz.

Hurmat bilan,  
Bilim ol jamoasi
"""
    user_msg = MIMEText(user_body)
    user_msg["Subject"] = "Izohingiz qabul qilindi"
    user_msg["From"] = SENDER_EMAIL
    user_msg["To"] = comment.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(admin_msg)
        server.send_message(user_msg)

    return {"message": "Izoh saqlandi va email yuborildi"}

@app.get("/users", response_model=List[UserOutput])
def get_users():
    return USERS