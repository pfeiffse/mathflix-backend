# app/core/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Mathflix Backend"
    DEBUG: bool = True

    JWT_SECRET: str = "SUPER_SECRET_KEY_2026"
    JWT_ALGO: str = "HS256"
    ACCESS_EXPIRE_MIN: int = 15
    REFRESH_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()