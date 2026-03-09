import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = os.environ.get("DB_PORT", 5432)
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False