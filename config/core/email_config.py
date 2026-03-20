# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "akande212@gmail.com"
    SMTP_PASSWORD: str = "qkub camd fuao rjrm"
    EMAIL_FROM: str = "akande212@gmail.com"
    FRONTEND_URL: str = "http://localhost:3000"


settings = Settings()
