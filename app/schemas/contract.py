from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from decimal import Decimal

# Propiedades compartidas
class ContractBase(BaseModel):
    arrendatario_id: int
    direccion: str
    tipo: str
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    servicios: Optional[str] = None
    clausulas_opcionales: Optional[Dict[str, Any]] = None

# Propiedades para creación (input)
class ContractCreate(ContractBase):
    pass

# Propiedades para actualización
class ContractUpdate(BaseModel):
    arrendatario_id: Optional[int] = None
    direccion: Optional[str] = None
    tipo: Optional[str] = None
    valor: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    servicios: Optional[str] = None
    clausulas_opcionales: Optional[Dict[str, Any]] = None

# Propiedades en base de datos (output)
class ContractInDBBase(ContractBase):
    id: int
    arrendador_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Propiedades a retornar vía API
class Contract(ContractInDBBase):
    pass
