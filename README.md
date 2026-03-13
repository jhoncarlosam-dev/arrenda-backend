# Arrenda API

Este es el proyecto backend para la gestión de contratos de arrendamiento y usuarios, construido con FastAPI, SQLAlchemy y JWT.

## Requisitos Previos
- Python 3.11+
- MySQL Server (ejecutándose localmente o en contenedor)
- Para la exportación a PNG: instalar `wkhtmltopdf` (y agregar `wkhtmltoimage` al PATH del entorno).

## Configuración Inicial

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate   
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar Variables de Entorno:**
   Verifica que el archivo `.env` en la raíz del proyecto tenga las credenciales correctas para tu base de datos local:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=password
   DB_NAME=app_db
   ```
   **Nota:** Asegúrate de crear manualmente la base de datos `app_db` en tu motor MySQL antes de continuar.

4. **Inicializar la Base de Datos:**
   Hemos provisto un script para crear las tablas utilizando los modelos definidos.
   ```bash
   python init_db.py
   ```

## Ejecución del Servidor

Arranca el servidor de desarrollo interactivamente mediante `uvicorn`:
```bash
uvicorn app.main:app --reload
```

## Documentación de la API

Una vez ejecutándose el servidor, puedes explorar e interactuar con la API directamente desde la interfaz Swagger auto-generada:
[http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

**NOTA**: Para ver la web de Swagger completa y amigable, puedes reemplazar temporalmente la inicialización en `app/main.py` de `openapi_url` por `docs_url="/docs"` o ingresar a la ruta `/docs` si la habilitas.
