from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

def init_db():
    print(f"Borrando tablas si existen en {settings.DB_NAME}...")
    # Base.metadata.drop_all(bind=engine)
    
    print(f"Creando tablas basadas en modelos en {settings.DB_NAME}...")
    Base.metadata.create_all(bind=engine)
    
    print("¡Base de datos inicializada exitosamente!")

if __name__ == "__main__":
    init_db()
