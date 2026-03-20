# app/services/email/email_service.py
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from services.email.email_client import EmailClient
from config.core.email_config import settings
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class EmailService:
    def __init__(self):
        self.client = EmailClient()

    def _render_template(self, template_name: str, context: dict):
        base_template = env.get_template("base.html")
        content_template = env.get_template(template_name)

        content = content_template.render(**context)

        return base_template.render(
            title=context.get("title", ""), content=content, year=datetime.utcnow().year
        )

    # ✅ Welcome Email
    def send_welcome_email(self, to_email: str, username: str):
        html = self._render_template(
            "welcome.html", {"title": "Welcome!", "username": username}
        )
        self.client.send_email(to_email, "Welcome to Our Platform 🎉", html)

    # ✅ Verify Email
    def send_verification_email(self, to_email: str, token: str):
        verify_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

        html = self._render_template(
            "verify_email.html",
            {"title": "Verify Your Email", "verify_link": verify_link},
        )

        self.client.send_email(to_email, "Verify Your Email", html)

    # ✅ Password Reset
    def send_password_reset_email(self, to_email: str, token: str):
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        html = self._render_template(
            "reset_password.html", {"title": "Reset Password", "reset_link": reset_link}
        )

        self.client.send_email(to_email, "Reset Your Password", html)

    # ✅ Custom Email (Order, etc.)
    def send_order_confirmation(self, to_email: str, username: str, order_id: str):
        html = self._render_template(
            "order_confirmation.html",
            {"title": "Order Confirmation", "username": username, "order_id": order_id},
        )

        self.client.send_email(to_email, "Order Confirmation", html)
