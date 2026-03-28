from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Numeric, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    arrendador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    arrendatario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    direccion = Column(String(255), nullable=False)
    tipo = Column(String(100), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    servicios = Column(Text, nullable=True)
    clausulas_opcionales = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True, default=None)

    # Relationships
    arrendador = relationship("User", foreign_keys=[arrendador_id])
    arrendatario = relationship("User", foreign_keys=[arrendatario_id])
