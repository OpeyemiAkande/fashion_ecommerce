# app/core/config.py
from pydantic_settings import BaseSettings
import os

smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
email_from = os.getenv("EMAIL_FROM")
frontend_url = os.getenv("FRONTEND_URL")
smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")


class Settings(BaseSettings):
    SMTP_HOST: str = smtp_host  # type: ignore
    SMTP_PORT: int = smtp_port  # type: ignore
    SMTP_USER: str = smtp_user  # type: ignore
    SMTP_PASSWORD: str = smtp_password  # type: ignore
    EMAIL_FROM: str = email_from  # type: ignore
    FRONTEND_URL: str = frontend_url  # type: ignore


settings = Settings()
