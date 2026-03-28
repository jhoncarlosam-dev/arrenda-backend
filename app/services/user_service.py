import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserProfileUpdate
from app.security.password import get_password_hash, verify_password

logger = logging.getLogger("arrenda.users")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        nombre=user.nombre,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_profile(db: Session, user: User, data: UserProfileUpdate) -> User:
    if data.email and data.email != user.email:
        if get_user_by_email(db, data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        user.email = data.email
        user.is_verified = False  # re-verify after email change

    if data.nombre is not None:
        user.nombre = data.nombre

    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: User, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    user.password = get_password_hash(new_password)
    db.commit()


def reset_password(db: Session, user_id: int, new_password: str) -> None:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.password = get_password_hash(new_password)
    db.commit()


def mark_email_verified(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_verified = True
    db.commit()


# ---------------------------------------------------------------------------
# Email delivery stub — replace with a real provider (SendGrid, SES, etc.)
# ---------------------------------------------------------------------------

def send_password_reset_email(email: str, token: str) -> None:
    """Logs the reset token. Swap this body for real email delivery."""
    logger.info("PASSWORD RESET TOKEN for %s → %s", email, token)


def send_verification_email(email: str, token: str) -> None:
    """Logs the verification token. Swap this body for real email delivery."""
    logger.info("EMAIL VERIFICATION TOKEN for %s → %s", email, token)
