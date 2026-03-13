from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, RoleEnum
from app.security.dependencies import get_current_user, require_role
from app.schemas.contract import ContractCreate, ContractUpdate, Contract
from app.services import contract_service

router = APIRouter()

@router.post("/", response_model=Contract, status_code=status.HTTP_201_CREATED, summary="Crear nuevo contrato")
def create_contract(
    *,
    db: Session = Depends(get_db),
    contract_in: ContractCreate,
    current_user: User = Depends(require_role(RoleEnum.ARRENDADOR.value)),
) -> Any:
    """
    Create new contract. Only ARRENDADOR can create.
    """
    contract = contract_service.create_contract(
        db=db, contract=contract_in, arrendador_id=current_user.id
    )
    return contract

@router.get("/{id}", response_model=Contract, summary="Obtener contrato por ID")
def read_contract(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get generic contract by ID.
    """
    contract = contract_service.get_contract(db=db, contract_id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    # Verificar que el usuario sea el arrendador o el arrendatario
    if (contract.arrendador_id != current_user.id and 
        contract.arrendatario_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions to access this contract"
        )
        
    return contract

@router.put("/{id}", response_model=Contract, summary="Actualizar contrato")
def update_contract(
    id: int,
    *,
    db: Session = Depends(get_db),
    contract_in: ContractUpdate,
    current_user: User = Depends(require_role(RoleEnum.ARRENDADOR.value)),
) -> Any:
    """
    Update a contract. Only ARRENDADOR can edit.
    """
    contract = contract_service.get_contract(db=db, contract_id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    # Verificar que sea SU contrato
    if contract.arrendador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only edit your own contracts"
        )
        
    contract = contract_service.update_contract(db=db, db_contract=contract, contract_in=contract_in)
    return contract
