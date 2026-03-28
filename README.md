# Arrenda — Gestión de Contratos de Arriendo

Sistema completo para la gestión de contratos de arrendamiento. Incluye un **backend REST API** construido con FastAPI + MySQL y un **frontend web** construido con React 18 + Vite. Soporta dos roles de usuario (arrendador y arrendatario) con autenticación JWT, gestión de cuentas y exportación de recibos en PDF/PNG.

---

## Estructura del Monorepo

```
arrenda-v2/
├── arrenda-backend/   # API REST — FastAPI + SQLAlchemy + MySQL
└── arrenda-frontend/  # Aplicación web — React 18 + Vite + TailwindCSS
```

---

## Stack Tecnológico

### Backend

| Capa | Tecnología |
|---|---|
| Framework | FastAPI 0.100+ |
| Servidor | Uvicorn |
| ORM | SQLAlchemy 2.0+ |
| Base de datos | MySQL 8.0 |
| Migraciones | Alembic |
| Autenticación | JWT (python-jose) |
| Hashing | Passlib / bcrypt |
| Validación | Pydantic 2.0+ |
| Rate limiting | SlowAPI |
| Exportación PDF | ReportLab |
| Exportación PNG | Pillow |
| Testing | Pytest + HTTPx |

### Frontend

| Capa | Tecnología |
|---|---|
| Framework | React 18 |
| Bundler | Vite 5 |
| Routing | React Router v6 |
| Formularios | React Hook Form |
| HTTP | Axios |
| Estilos | TailwindCSS 3 |
| Notificaciones | react-hot-toast |
| Estado global | Context API |

---

## Roles y Permisos

| Acción | ARRENDADOR | ARRENDATARIO |
|---|---|---|
| Registrar e iniciar sesión | ✅ | ✅ |
| Ver y editar perfil | ✅ | ✅ |
| Cambiar contraseña | ✅ | ✅ |
| Verificar correo | ✅ | ✅ |
| **Crear contrato** | ✅ | ❌ |
| **Editar contrato propio** | ✅ | ❌ |
| **Eliminar contrato propio** | ✅ | ❌ |
| Ver contratos | ✅ | ✅ |
| **Exportar recibo PDF/PNG** | ❌ | ✅ |

---

## Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- MySQL Server 8.0 (local o en contenedor Docker)

---

### Backend

#### 1. Entorno virtual e instalación

```bash
cd arrenda-backend

python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

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

#### 3. Inicializar la base de datos

```bash
python init_db.py
```

#### 4. Levantar el servidor

```bash
uvicorn app.main:app --reload
# API disponible en http://localhost:8000
```

---

### Frontend

#### 1. Instalar dependencias

```bash
cd arrenda-frontend
npm install
```

#### 2. Variables de entorno

```bash
cp .env.example .env
```

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

#### 3. Levantar el servidor de desarrollo

```bash
npm run dev
# Aplicación disponible en http://localhost:5173
```

#### 4. Build de producción

```bash
npm run build
```

---

### Docker (Backend + MySQL)

Levanta la API y MySQL con un solo comando:

```bash
cd arrenda-backend
docker-compose up --build
```

- API: `http://localhost:8000`
- MySQL: `localhost:3306`

La API espera a que MySQL esté saludable antes de arrancar.

---

## Estructura del Backend

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
│   │   ├── user.py             # Modelo User
│   │   └── contract.py         # Modelo Contract (soft delete)
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
│   └── main.py                 # Inicialización de la app FastAPI
├── migrations/                 # Migraciones Alembic
├── tests/                      # Suite de pruebas
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── init_db.py
└── requirements.txt
```

## Estructura del Frontend

```
arrenda-frontend/
├── src/
│   ├── api/
│   │   ├── axios.js            # Instancia Axios con interceptores JWT
│   │   ├── authApi.js          # login, register
│   │   ├── usersApi.js         # perfil, contraseña, verificación de email
│   │   ├── contractsApi.js     # CRUD de contratos
│   │   └── receiptsApi.js      # Exportación PDF/PNG (descarga automática)
│   ├── auth/
│   │   └── AuthContext.jsx     # Contexto JWT: login/logout/roles
│   ├── components/
│   │   ├── layout/             # Navbar, Sidebar, Layout
│   │   ├── ui/                 # Button, Input, Modal, Pagination, Badge...
│   │   └── contracts/          # ContractCard, ContractForm
│   ├── pages/
│   │   ├── auth/               # Login, Register, ForgotPassword, ResetPassword, VerifyEmail
│   │   ├── contracts/          # ContractsPage, ContractDetailPage
│   │   ├── profile/            # ProfilePage
│   │   └── DashboardPage.jsx
│   ├── routes/                 # PrivateRoute, AppRoutes
│   ├── utils/                  # formatters.js, validators.js
│   └── main.jsx                # Entry point
├── public/
├── .env.example
├── package.json
├── tailwind.config.js
└── vite.config.js
```

---

## Endpoints de la API

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
| `GET` | `/contracts/{id}` | Obtener contrato por ID | Partes del contrato |
| `PUT` | `/contracts/{id}` | Actualizar contrato | ARRENDADOR (propietario) |
| `DELETE` | `/contracts/{id}` | Eliminar contrato (soft delete) | ARRENDADOR (propietario) |

### Exportación de Recibos

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| `GET` | `/receipts/{id}/export/pdf` | Exportar recibo como PDF | ARRENDATARIO |
| `GET` | `/receipts/{id}/export/png` | Exportar recibo como PNG | ARRENDATARIO |

**Paginación:** `?skip=0&limit=20` (máximo 100 por página)

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
| `tipo` | String | Tipo: residencial / comercial / mixto |
| `valor` | Numeric(10,2) | Valor mensual del arriendo |
| `servicios` | Text (nullable) | Servicios incluidos |
| `clausulas_opcionales` | JSON (nullable) | Cláusulas adicionales |
| `created_at` | DateTime | Fecha de creación (UTC) |
| `deleted_at` | DateTime (nullable) | Soft delete |

---

## Autenticación JWT

- **Algoritmo:** HS256
- **Expiración del token:** 30 minutos (configurable)
- **Header:** `Authorization: Bearer <token>`
- **Payload:** `{ user_id, role, exp }`

Tokens de propósito especial (reset de contraseña: 1h, verificación de email: 24h) usan un campo `purpose` adicional.

---

## Documentación Interactiva

Con el backend corriendo:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI JSON: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## Pruebas

```bash
cd arrenda-backend
pytest
```
