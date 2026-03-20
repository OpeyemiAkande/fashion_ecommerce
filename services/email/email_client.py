# app/services/email/email_client.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.core.email_config import settings


class EmailClient:
    def send_email(self, to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
