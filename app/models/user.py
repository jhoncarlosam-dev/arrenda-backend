import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    ARRENDADOR = "ARRENDADOR"
    ARRENDATARIO = "ARRENDATARIO"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
