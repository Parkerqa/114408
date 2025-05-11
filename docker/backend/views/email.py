import os

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from schemas.user import PasswordForget

conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = os.environ.get("MAIL_FROM"),
    MAIL_PORT = os.environ.get("MAIL_PORT"),
    MAIL_SERVER = os.environ.get("MAIL_SERVER"),
    MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fm = FastMail(conf)

# send reset password url to user email
async def send_email(email, new_password: str) -> bool:
    html = f"""<p>您的新密碼：{new_password}</p> """

    message = MessageSchema(
        subject="新的 TicketTransformer 密碼",
        recipients=[email],
        body=html,
        subtype=MessageType.html)
    try:
        await fm.send_message(message)
        return True
    except Exception as e:
        print(e)
        return False