from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.limiter import limiter
from app.middleware.logging import log_requests
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

_is_dev = settings.ENV != "production"

app = FastAPI(
    title="Arrenda API",
    description=DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs" if _is_dev else None,
    redoc_url="/redoc" if _is_dev else None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if _is_dev else None,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Request logging
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
