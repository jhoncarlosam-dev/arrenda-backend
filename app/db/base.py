from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Interesante para migraciones con Alembic: importar todos los modelos aquí
from app.models.user import User
from app.models.contract import Contract
