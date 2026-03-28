"""
Short-lived, purpose-scoped tokens for password reset and email verification.
Uses the same SECRET_KEY / ALGORITHM as auth JWTs but adds a 'purpose' claim
so tokens cannot be cross-used.
"""
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.config import settings

PURPOSE_PASSWORD_RESET = "password_reset"
PURPOSE_EMAIL_VERIFY = "email_verify"

_EXPIRY = {
    PURPOSE_PASSWORD_RESET: timedelta(hours=1),
    PURPOSE_EMAIL_VERIFY: timedelta(hours=24),
}


def create_scoped_token(user_id: int, purpose: str) -> str:
    expire = datetime.now(timezone.utc) + _EXPIRY[purpose]
    return jwt.encode(
        {"sub": str(user_id), "purpose": purpose, "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_scoped_token(token: str, expected_purpose: str) -> int:
    """Returns user_id or raises 400."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    if payload.get("purpose") != expected_purpose:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token purpose")

    return int(payload["sub"])
