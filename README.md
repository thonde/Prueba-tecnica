# Auth API

API de autenticación y autorización construida con FastAPI, SQLModel y JWT.

## Requisitos

- Python 3.12+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=sqlite:///./auth.db
JWT_SECRET_KEY=tu-clave-secreta
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPassword123!
ADMIN_NAME=Admin
```

## Ejecución

```bash
python run.py
```

Esto crea la base de datos, carga los datos iniciales (permisos, rol admin, usuario admin) y levanta el servidor en `http://127.0.0.1:8000`.

Documentación de la API disponible en `http://127.0.0.1:8000/docs`.

## Docker (opcional)

```bash
docker compose up --build
```

## Tests

```bash
pytest tests/ -v
```

## Credenciales del administrador por defecto

- Email: `admin@example.com`
- Contraseña: `AdminPassword123!`
