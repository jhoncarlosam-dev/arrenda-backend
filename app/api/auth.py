from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.schemas.token import Token, LoginRequest
from app.services.user_service import get_user_by_email
from app.security.password import verify_password
from app.security.jwt import create_access_token

router = APIRouter()

@router.post("/login", response_model=Token, summary="Autenticación y generación de JWT")
def login(db: Session = Depends(get_db), login_data: LoginRequest = None):
    """
    Login endpoint that doesn't use OAuth2 form data
    """
    user = get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Token payload containing user_id and role as requested
    token_payload = {
        "user_id": user.id,
        "role": user.role.value
    }
    
    access_token = create_access_token(
        data=token_payload, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
