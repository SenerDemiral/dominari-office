# fastapi-app/services/mail_service.py
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME = "sener@dominari.cloud",
    MAIL_PASSWORD = "ftol qhgz dhiv akxs", # Buraya o 16 haneli kodu yazacaksın
    MAIL_FROM = "info@dominari.cloud",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True
)

async def send_welcome_email_task(email: str, name: str, temp_pwd: str):
    message = MessageSchema(
        subject="Dominari Cloud Giriş Bilgileri",
        recipients=[email],
        body=f"Merhaba {name}, geçici şifreniz: {temp_pwd}",
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)