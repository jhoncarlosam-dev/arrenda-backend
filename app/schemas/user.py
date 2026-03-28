from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from app.models.user import RoleEnum

# Propiedades compartidas
class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    role: RoleEnum

# Propiedades para creación (input)
class UserCreate(UserBase):
    password: str

# Actualizar solo perfil (nombre / email) — sin rol ni contraseña
class UserProfileUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None

# Cambio de contraseña autenticado
class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def new_password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

# Flujo de reset de contraseña
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def new_password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

# Confirmar verificación de email
class EmailVerificationConfirm(BaseModel):
    token: str

# Propiedades para actualización (legacy — mantener compatibilidad)
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = None

# Propiedades en base de datos (output)
class UserInDBBase(UserBase):
    id: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Propiedades a retornar vía API
class User(UserInDBBase):
    pass

# Propiedades almacenadas en DB
class UserInDB(UserInDBBase):
    password: str
