from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.user import (
    UserCreate,
    User,
    UserProfileUpdate,
    PasswordChange,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerificationConfirm,
)
from app.services import user_service
from app.security.dependencies import get_current_user
from app.security.tokens import (
    create_scoped_token,
    decode_scoped_token,
    PURPOSE_PASSWORD_RESET,
    PURPOSE_EMAIL_VERIFY,
)

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    if user_service.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    return user_service.create_user(db, user=user_in)


@router.get("/me", response_model=User, summary="Obtener perfil propio")
def read_me(current_user: UserModel = Depends(get_current_user)) -> Any:
    return current_user


@router.patch("/me", response_model=User, summary="Actualizar perfil propio")
def update_me(
    *,
    db: Session = Depends(get_db),
    data: UserProfileUpdate,
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    return user_service.update_profile(db, user=current_user, data=data)


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT, summary="Cambiar contraseña")
def change_password(
    *,
    db: Session = Depends(get_db),
    body: PasswordChange,
    current_user: UserModel = Depends(get_current_user),
) -> None:
    user_service.change_password(db, user=current_user, current_password=body.current_password, new_password=body.new_password)


# ---------------------------------------------------------------------------
# Password reset (unauthenticated flow)
# ---------------------------------------------------------------------------

@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED, summary="Solicitar reset de contraseña")
def password_reset_request(body: PasswordResetRequest, db: Session = Depends(get_db)) -> dict:
    user = user_service.get_user_by_email(db, email=body.email)
    if user:
        token = create_scoped_token(user.id, PURPOSE_PASSWORD_RESET)
        user_service.send_password_reset_email(user.email, token)
    # Always return 202 to avoid leaking which emails are registered
    return {"detail": "If that email is registered you will receive a reset link shortly."}


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT, summary="Confirmar reset de contraseña")
def password_reset_confirm(body: PasswordResetConfirm, db: Session = Depends(get_db)) -> None:
    user_id = decode_scoped_token(body.token, PURPOSE_PASSWORD_RESET)
    user_service.reset_password(db, user_id=user_id, new_password=body.new_password)


# ---------------------------------------------------------------------------
# Email verification
# ---------------------------------------------------------------------------

@router.post("/me/verify-email/request", status_code=status.HTTP_202_ACCEPTED, summary="Solicitar verificación de email")
def verify_email_request(current_user: UserModel = Depends(get_current_user)) -> dict:
    if current_user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already verified")
    token = create_scoped_token(current_user.id, PURPOSE_EMAIL_VERIFY)
    user_service.send_verification_email(current_user.email, token)
    return {"detail": "Verification email sent."}


@router.post("/verify-email/confirm", status_code=status.HTTP_204_NO_CONTENT, summary="Confirmar verificación de email")
def verify_email_confirm(body: EmailVerificationConfirm, db: Session = Depends(get_db)) -> None:
    user_id = decode_scoped_token(body.token, PURPOSE_EMAIL_VERIFY)
    user_service.mark_email_verified(db, user_id=user_id)


@router.get("/{user_id}", response_model=User, summary="Obtener usuario por ID")
def read_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)) -> Any:
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
