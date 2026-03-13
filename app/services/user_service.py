from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.security.password import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    # Hash de la contraseña
    hashed_password = get_password_hash(user.password)
    
    # Crear modelo User
    db_user = User(
        nombre=user.nombre,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    
    # Guardar en base de datos
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
