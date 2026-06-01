# FSTR Mountain Passes API

REST API для регистрации и модерации горных перевалов. Разработано в рамках стажировки ФСТР.

---

## Описание задачи

Туристы через мобильное приложение отправляют данные о пройденных перевалах:
- Координаты и высота
- Фотографии
- Информация о пользователе (ФИО, email, телефон)
- Категория трудности по сезонам

**Система решает:**
1. Приём данных о перевалах через REST API
2. Сохранение со статусом `new` (ожидание модерации)
3. Получение и редактирование записей
4. Блокировку изменений, если статус ≠ `new`
5. Фиксацию времени создания и обновления записей (`created_at`/`updated_at`)

---

## Реализованный функционал

### Спринт 1: Базовый функционал
| Метод | Описание | Статус |
|-------|----------|--------|
| POST /submitData | Добавление нового перевала со статусом new | Готово |

### Спринт 2: Расширенный функционал
| Метод | Описание | Статус |
|-------|----------|--------|
| GET /submitData/{id} | Получение полной информации о перевале по ID | Готово |
| PATCH /submitData/{id} | Редактирование перевала (только если status="new") | Готово |
| GET /submitData/?user__email=<email> | Список всех перевалов пользователя | Готово |

### Бизнес-логика
- При создании перевала автоматически устанавливается status="new"
- Редактирование запрещено, если статус не равен new (pending/accepted/rejected)
- При редактировании нельзя менять данные пользователя (ФИО, email, телефон)
- Все настройки БД читаются из переменных окружения (FSTR_DB_*)
- Валидация входных данных через Pydantic (email, координаты, обязательные поля)

---

## Технологии

| Компонент | Технология | Версия |
|-----------|------------|--------|
| Фреймворк | FastAPI | 0.109.0 |
| ORM | SQLAlchemy | 2.0.25 |
| База данных | PostgreSQL | 14+ |
| Валидация | Pydantic | 2.5.0 |
| Сервер | Uvicorn (ASGI) | 0.27.0 |
| Конфигурация | python-dotenv, pydantic-settings | 1.0.0+ |

---

## Установка и запуск (локально)

### 1. Клонирование репозитория
git clone https://github.com/horizonborder1-design/fstr_sprint2.git
cd fstr_sprint2

### 2. Создание виртуального окружения
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

### 3. Установка зависимостей
pip install -r requirements.txt

### 4. Настройка переменных окружения
Создай файл .env в корне проекта на основе .env.example:

# === PostgreSQL настройки ===
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=your_secure_password
FSTR_DB_NAME=fstr_db

### 5. Создание базы данных
# Через psql
psql -h localhost -U postgres -d fstr_db -f database_schema.sql

# Или через pgAdmin: открой Query Tool → вставь содержимое файла → Execute

### 6. Запуск сервера
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Сервер запустится по адресу: http://127.0.0.1:8000

---

## API Endpoints

### POST /submitData — Добавить новый перевал

Запрос:
POST /submitData
Content-Type: application/json

Тело запроса (JSON):
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22T13:18:13",
  "user": {
    "email": "user@email.tld",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+79031234567"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": []
}

Ответ (успех):
{
  "status": 200,
  "message": null,
  "id": 42
}

Ответ (ошибка):
{
  "status": 400,
  "message": "Bad Request: missing required fields",
  "id": null
}

---

### GET /submitData/{id} — Получить перевал по ID

Пример запроса:
GET /submitData/42

Ответ:
{
  "id": 42,
  "title": "Пхия",
  "status": "new",
  "latitude": 45.3842,
  "longitude": 7.1525,
  "user": {
    "email": "user@email.tld",
    "fam": "Пупкин",
    ...
  },
  "images": []
}

---

### PATCH /submitData/{id} — Редактировать перевал

Пример запроса:
PATCH /submitData/42
Content-Type: application/json

{
  "title": "Новое название",
  "height": 1250,
  "user": { ... }
}

Ответ (успех):
{
  "state": 1,
  "message": "Запись успешно обновлена"
}

Ответ (ошибка — статус не new):
{
  "state": 0,
  "message": "Редактирование невозможно. Текущий статус: accepted"
}

---

### GET /submitData/?user__email=<email> — Список перевалов пользователя

Пример запроса:
GET /submitData/?user__email=user@email.tld

Ответ:
[
  {
    "id": 42,
    "title": "Пхия",
    "status": "new",
    ...
  },
  {
    "id": 43,
    "title": "Другой перевал",
    "status": "pending",
    ...
  }
]

---

## Тестирование

### Интерактивная документация (Swagger)
После запуска сервера открой в браузере:
- http://127.0.0.1:8000/docs — Swagger UI
- http://127.0.0.1:8000/redoc — ReDoc

Здесь можно протестировать все эндпоинты без написания кода.

### Проверка через curl
# Получить перевал с ID=1
curl http://127.0.0.1:8000/submitData/1

# Получить все перевалы пользователя
curl "http://127.0.0.1:8000/submitData/?user__email=user@email.tld"

---

## Структура базы данных

users
├── id (PK)
├── email (unique)
├── fam, name, otc, phone
└── created_at

passes
├── id (PK)
├── title, beauty_title, other_titles, connect
├── latitude, longitude, height
├── level_winter/spring/summer/autumn
├── status (new/pending/accepted/rejected) ← ключевое поле
├── user_id (FK → users)
└── created_at, updated_at

pass_images
├── id (PK)
── pass_id (FK → passes, CASCADE)
├── data (BYTEA), title
└── added_at

---

## Структура проекта

fstr_sprint2/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI приложение, эндпоинты
│   ├── database.py      # Подключение к БД
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы валидации
│   ├── crud.py          # Класс DatabaseManager (бизнес-логика)
│   └── config.py        # Настройки из переменных окружения
├── .env.example         # Шаблон переменных окружения
├── database_schema.sql  # SQL-скрипт создания таблиц
├── requirements.txt     # Зависимости Python
├── README.md            # Файл описание
└── .gitignore           # Исключения для Git

---

## Автор
📧 khristiukip@gmail.com
🔗 GitHub: https://github.com/horizonborder1-design