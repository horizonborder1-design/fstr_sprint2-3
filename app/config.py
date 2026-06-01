import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Явно указываем путь к .env файлу
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_login: str = "postgres"
    db_pass: str = "postgres"
    db_name: str = "fstr_db"
    
    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        env_prefix = "FSTR_DB_"

# Создаём экземпляр настроек
settings = Settings()