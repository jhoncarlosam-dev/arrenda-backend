from pydantic import BaseModel, EmailStr
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

# Propiedades para actualización
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = None

# Propiedades en base de datos (output)
class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Propiedades a retornar vía API
class User(UserInDBBase):
    pass

# Propiedades almacenadas en DB
class UserInDB(UserInDBBase):
    password: str
