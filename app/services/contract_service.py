from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate


def _active(db: Session):
    """Base query that excludes soft-deleted contracts."""
    return db.query(Contract).filter(Contract.deleted_at.is_(None))


def get_contract(db: Session, contract_id: int):
    return _active(db).filter(Contract.id == contract_id).first()


def get_contracts_by_arrendador(db: Session, arrendador_id: int, skip: int = 0, limit: int = 20):
    q = _active(db).filter(Contract.arrendador_id == arrendador_id)
    return q.offset(skip).limit(limit).all(), q.count()


def get_contracts_by_arrendatario(db: Session, arrendatario_id: int, skip: int = 0, limit: int = 20):
    q = _active(db).filter(Contract.arrendatario_id == arrendatario_id)
    return q.offset(skip).limit(limit).all(), q.count()


def create_contract(db: Session, contract: ContractCreate, arrendador_id: int):
    db_contract = Contract(
        arrendador_id=arrendador_id,
        arrendatario_id=contract.arrendatario_id,
        direccion=contract.direccion,
        tipo=contract.tipo,
        valor=contract.valor,
        servicios=contract.servicios,
        clausulas_opcionales=contract.clausulas_opcionales,
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def update_contract(db: Session, db_contract: Contract, contract_in: ContractUpdate):
    for field, value in contract_in.model_dump(exclude_unset=True).items():
        setattr(db_contract, field, value)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def delete_contract(db: Session, contract_id: int) -> None:
    contract = _active(db).filter(Contract.id == contract_id).first()
    if contract:
        contract.deleted_at = datetime.now(timezone.utc)
        db.commit()
