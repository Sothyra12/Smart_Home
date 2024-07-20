from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
# You might need to implement or import an email sending function
# from app.utils import send_email

def authenticate(db: Session, email: str, password: str) -> models.User:
    user = crud.user.get_user_by_email(db, email=email)
    print("user")
    print(user)
    if not user:
        return None
    if not security.verify_password(password, user.password_hash):
        return None
    return user

def send_reset_password_email(email_to: str, email: str, token: str):
    subject = f"Password recovery for user {email}"
    with open(settings.EMAIL_TEMPLATES_DIR / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )