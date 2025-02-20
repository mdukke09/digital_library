![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.4.2-e92063.svg)
# Digital Library API

API REST para gestión de biblioteca digital desarrollada con FastAPI y PostgreSQL.

## Características

- Gestión de usuarios, autores y libros
- Sistema de préstamos de libros
- Autenticación mediante JWT
- Documentación automática con Swagger UI
- Tests unitarios
- Principios SOLID y Clean Code

## Tecnologías Utilizadas

- FastAPI (Framework web)
- PostgreSQL (Base de datos)
- SQLAlchemy (ORM)
- Pydantic (Validación de datos)
- JWT (Autenticación)
- Pytest (Testing)
- Alembic (Migraciones)
- Python 3.12

## Requisitos

- Python 3.8+
- PostgreSQL (se recomienda usar Render.com para la base de datos)
- pip (gestor de paquetes de Python)

## Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone https://github.com/mdukke09/digital_library.git
cd digital-library-api
```

2. Crear y activar entorno virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar base de datos:
   - Crear cuenta en Render.com
   - Crear nueva base de datos PostgreSQL
   - Obtener credenciales de conexión

5. Crear archivo `.env` con las siguientes variables:
```plaintext
# Configuración del Proyecto
PROJECT_NAME=Digital Library API
VERSION=1.0.0
API_V1_STR=/api/v1

# PostgreSQL
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=your-db.render.com
POSTGRES_DB=your_db
POSTGRES_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}

# Seguridad
JWT_SECRET=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=11520
```

6. Ejecutar migraciones:
```bash
# Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migración
alembic upgrade head
```

## Estructura del Proyecto

```
digital_library/
├── alembic/                    # Migraciones de base de datos
├── app/
│   ├── api/                   # Endpoints API
│   ├── core/                  # Configuración central
│   ├── crud/                  # Operaciones CRUD
│   ├── models/                # Modelos SQLAlchemy
│   ├── schemas/               # Esquemas Pydantic
│   └── services/             # Servicios de negocio
├── tests/                     # Tests
└── requirements.txt          # Dependencias
```

## Ejecución

1. Iniciar servidor de desarrollo:
```bash
uvicorn app.main:app --reload
```

2. Acceder a la documentación:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Tests

Ejecutar tests:
```bash
pytest -v
```

Ver cobertura de tests:
```bash
pytest --cov=app tests/
```

## Desarrollo

### Agregar Nuevos Modelos

1. Crear modelo en `app/models/`
2. Crear esquema en `app/schemas/`
3. Crear operaciones CRUD en `app/crud/`
4. Crear endpoints en `app/api/v1/endpoints/`
5. Generar y aplicar migraciones:
```bash
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
```

### Configuración de Base de Datos

La conexión a la base de datos se gestiona a través de SQLAlchemy y se configura en `app/core/config.py`. Asegúrate de que las variables de entorno estén correctamente configuradas en el archivo `.env`.

### Autenticación

La API utiliza autenticación JWT. Los tokens se generan al iniciar sesión y deben incluirse en el encabezado de las solicitudes:
```
Authorization: Bearer <token>
```

## Documentación API

La documentación completa de la API está disponible en:
- `/docs` - Swagger UI
- `/redoc` - ReDoc

Incluye:
- Endpoints disponibles
- Esquemas de datos
- Ejemplos de uso
- Códigos de respuesta

## Endpoints Principales

### Autores
- `GET /api/v1/authors` - Listar autores
- `POST /api/v1/authors` - Crear autor
- `GET /api/v1/authors/{id}` - Obtener autor
- `PUT /api/v1/authors/{id}` - Actualizar autor
- `DELETE /api/v1/authors/{id}` - Eliminar autor

### Libros
- `GET /api/v1/books` - Listar libros
- `POST /api/v1/books` - Crear libro
- `GET /api/v1/books/{id}` - Obtener libro
- `PUT /api/v1/books/{id}` - Actualizar libro
- `DELETE /api/v1/books/{id}` - Eliminar libro
- `POST /api/v1/books/{id}/borrow` - Prestar libro
- `POST /api/v1/books/{id}/return` - Devolver libro
- `GET /api/v1/books/search` - Buscar libros

### Usuarios
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/users` - Listar usuarios
- `POST /api/v1/users` - Crear usuario
- `GET /api/v1/users/{id}` - Obtener usuario
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `DELETE /api/v1/users/{id}` - Eliminar usuario