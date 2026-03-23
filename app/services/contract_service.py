from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate

def get_contract(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_contracts_by_arrendador(db: Session, arrendador_id: int, skip: int = 0, limit: int = 100):
    return db.query(Contract)\
        .filter(Contract.arrendador_id == arrendador_id)\
        .offset(skip).limit(limit).all()

def get_contracts_by_arrendatario(db: Session, arrendatario_id: int, skip: int = 0, limit: int = 100):
    return db.query(Contract)\
        .filter(Contract.arrendatario_id == arrendatario_id)\
        .offset(skip).limit(limit).all()

def create_contract(db: Session, contract: ContractCreate, arrendador_id: int):
    db_contract = Contract(
        arrendador_id=arrendador_id,
        arrendatario_id=contract.arrendatario_id,
        direccion=contract.direccion,
        tipo=contract.tipo,
        valor=contract.valor,
        servicios=contract.servicios,
        clausulas_opcionales=contract.clausulas_opcionales
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def update_contract(db: Session, db_contract: Contract, contract_in: ContractUpdate):
    update_data = contract_in.model_dump(exclude_unset=True)

    for field in update_data:
        setattr(db_contract, field, update_data[field])

    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def delete_contract(db: Session, contract_id: int) -> None:
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        db.delete(contract)
        db.commit()
