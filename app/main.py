from fastapi import FastAPI
from app.core.config import settings
from app.api import users, auth, contracts, export
from app.api.error_handlers import setup_exception_handlers

DESCRIPTION = """
API para la gestión de sistema de arrendamiento.
Permite administrar:
* **Autenticación** y manejo de roles. 🔒
* **Usuarios** (Arrendadores y Arrendatarios). 👤
* **Contratos** de forma segura. 📄
* **Exportación** de recibos en formato PDF y PNG. 📥
"""

app = FastAPI(
    title="Arrenda API",
    description=DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Initialize global error handlers
setup_exception_handlers(app)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(contracts.router, prefix=f"{settings.API_V1_STR}/contracts", tags=["contracts"])
app.include_router(export.router, prefix=f"{settings.API_V1_STR}/receipts", tags=["receipts"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
