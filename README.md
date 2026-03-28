# Arrenda API

Backend para la gestión de contratos de arrendamiento, construido con **FastAPI**, **SQLAlchemy** y **MySQL**. Soporta dos roles de usuario: arrendador y arrendatario, con autenticación JWT, gestión de cuentas por email y exportación de recibos en PDF/PNG.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Framework | FastAPI 0.100+ |
| Servidor | Uvicorn |
| ORM | SQLAlchemy 2.0+ |
| Base de datos | MySQL 8.0 |
| Migraciones | Alembic |
| Autenticación | JWT (python-jose) |
| Hashing | Passlib/bcrypt |
| Validación | Pydantic 2.0+ |
| Rate limiting | SlowAPI |
| Exportación PDF | ReportLab |
| Exportación PNG | Pillow |
| Testing | Pytest + HTTPx |

---

## Estructura del Proyecto

```
arrenda-backend/
├── app/
│   ├── api/                    # Rutas HTTP
│   │   ├── auth.py             # Login
│   │   ├── users.py            # Gestión de usuarios y cuenta
│   │   ├── contracts.py        # CRUD de contratos
│   │   ├── export.py           # Exportación PDF/PNG
│   │   └── error_handlers.py   # Manejo global de errores
│   ├── core/
│   │   ├── config.py           # Configuración y variables de entorno
│   │   ├── limiter.py          # Rate limiting
│   │   └── pagination.py       # Utilidades de paginación
│   ├── db/
│   │   ├── base.py             # Base declarativa SQLAlchemy
│   │   └── session.py          # Gestión de sesiones DB
│   ├── export/
│   │   ├── pdf_service.py      # Generación de PDFs
│   │   └── png_service.py      # Generación de PNGs
│   ├── middleware/
│   │   └── logging.py          # Logging de requests
│   ├── models/
│   │   ├── user.py             # Modelo User (roles: ARRENDADOR | ARRENDATARIO)
│   │   └── contract.py         # Modelo Contract
│   ├── schemas/
│   │   ├── user.py             # Schemas de usuario
│   │   ├── contract.py         # Schemas de contrato
│   │   └── token.py            # Schemas JWT
│   ├── security/
│   │   ├── jwt.py              # Creación y verificación de tokens
│   │   ├── password.py         # Hashing de contraseñas
│   │   ├── tokens.py           # Tokens con propósito (reset, verificación)
│   │   └── dependencies.py     # Dependencias de autenticación y roles
│   ├── services/
│   │   ├── user_service.py     # Lógica de negocio de usuarios
│   │   └── contract_service.py # Lógica de negocio de contratos
│   ├── utils/
│   │   └── exceptions.py       # Excepciones personalizadas
│   └── main.py                 # Inicialización de la app FastAPI
├── migrations/                 # Migraciones Alembic
├── tests/                      # Suite de pruebas
├── .env.example                # Plantilla de variables de entorno
├── alembic.ini                 # Configuración de Alembic
├── docker-compose.yml          # Orquestación con Docker
├── Dockerfile                  # Imagen Docker
├── init_db.py                  # Script de inicialización de la DB
└── requirements.txt            # Dependencias Python
```

---

## Requisitos Previos

- Python 3.11+
- MySQL Server (local o en contenedor)

---

## Configuración Local

### 1. Entorno virtual

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Variables de entorno

Copia el archivo de ejemplo y edítalo con tus credenciales:

```bash
cp .env.example .env
```

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=<tu_contraseña>
DB_NAME=arrenda_db

SECRET_KEY=<clave-secreta-larga-y-aleatoria>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

VERSION=1.0.0
API_V1_STR=/api/v1
```

> Crea manualmente la base de datos `arrenda_db` en MySQL antes de continuar.

### 4. Inicializar la base de datos

```bash
python init_db.py
```

### 5. Levantar el servidor

```bash
uvicorn app.main:app --reload
```

---

## Docker

Levanta la API y MySQL con un solo comando:

```bash
docker-compose up --build
```

- API disponible en: `http://localhost:8000`
- MySQL disponible en: `localhost:3306`

La API espera a que MySQL esté saludable antes de arrancar.

---

## Documentación de la API

Con el servidor corriendo, accede a la interfaz interactiva:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI JSON: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## Endpoints

Todos los endpoints tienen el prefijo `/api/v1`.

### Autenticación

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| `POST` | `/auth/login` | Login con email y contraseña, retorna JWT | Público |

### Usuarios

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| `POST` | `/users/` | Registrar nuevo usuario | Público |
| `GET` | `/users/me` | Obtener perfil propio | Autenticado |
| `PATCH` | `/users/me` | Actualizar nombre o email | Autenticado |
| `POST` | `/users/me/password` | Cambiar contraseña | Autenticado |
| `GET` | `/users/{user_id}` | Obtener usuario por ID | Autenticado |
| `POST` | `/users/me/verify-email/request` | Solicitar verificación de email | Autenticado |
| `POST` | `/users/verify-email/confirm` | Confirmar email con token | Público |
| `POST` | `/users/password-reset/request` | Solicitar restablecimiento de contraseña | Público |
| `POST` | `/users/password-reset/confirm` | Confirmar nueva contraseña con token | Público |

### Contratos

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| `POST` | `/contracts/` | Crear contrato | ARRENDADOR |
| `GET` | `/contracts/me` | Listar contratos propios (paginado) | Autenticado |
| `GET` | `/contracts/{id}` | Obtener contrato por ID | Arrendador o Arrendatario del contrato |
| `PUT` | `/contracts/{id}` | Actualizar contrato | ARRENDADOR (propietario) |
| `DELETE` | `/contracts/{id}` | Eliminar contrato (soft delete) | ARRENDADOR (propietario) |

### Exportación de Recibos

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| `GET` | `/receipts/{id}/export/pdf` | Exportar recibo como PDF | ARRENDATARIO |
| `GET` | `/receipts/{id}/export/png` | Exportar recibo como PNG | ARRENDATARIO |

---

## Modelos de Base de Datos

### User

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador único |
| `nombre` | String | Nombre completo |
| `email` | String (unique) | Correo electrónico |
| `password` | String | Contraseña hasheada (bcrypt) |
| `role` | Enum | `ARRENDADOR` o `ARRENDATARIO` |
| `is_verified` | Boolean | Estado de verificación de email |
| `created_at` | DateTime | Fecha de creación (UTC) |

### Contract

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador único |
| `arrendador_id` | FK → users | ID del arrendador |
| `arrendatario_id` | FK → users | ID del arrendatario |
| `direccion` | String | Dirección del inmueble |
| `tipo` | String | Tipo de inmueble |
| `valor` | Numeric(10,2) | Valor del arriendo |
| `servicios` | Text (nullable) | Servicios incluidos |
| `clausulas_opcionales` | JSON (nullable) | Cláusulas adicionales |
| `created_at` | DateTime | Fecha de creación (UTC) |
| `deleted_at` | DateTime (nullable) | Fecha de eliminación (soft delete) |

---

## Roles y Permisos

| Acción | ARRENDADOR | ARRENDATARIO |
|---|---|---|
| Crear contrato | ✅ | ❌ |
| Editar contrato propio | ✅ | ❌ |
| Eliminar contrato propio | ✅ | ❌ |
| Ver contratos propios | ✅ | ✅ |
| Exportar recibo (PDF/PNG) | ❌ | ✅ |

---

## Pruebas

```bash
pytest
```
