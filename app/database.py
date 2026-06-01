from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Формируем строку подключения на основе настроек из config.py
DATABASE_URL = f"postgresql://{settings.db_login}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Создаем движок (Engine) для соединения с БД
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для наших моделей (таблиц)
Base = declarative_base()

# Функция-генератор для получения сессии БД (используется в FastAPI для зависимости)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()