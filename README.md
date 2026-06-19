# Auth API

Authentication and authorization API built with FastAPI, SQLModel and JWT.

## Tech Stack

- **Python** 3.14
- **FastAPI** (ASGI framework)
- **SQLModel** 0.0.38 (SQLAlchemy 2.0 + Pydantic)
- **PyJWT** 2.13.0 (JSON Web Tokens)
- **bcrypt** 4.3.0 (password hashing)
- **SQLite** (database)
- **Docker** (containerization)

## Project Structure

```
app/
├── config/          # Settings and security
├── db/              # Database connection
├── models/          # Database tables
├── schemas/         # Request/response validation
├── services/        # Business logic
├── routers/         # API endpoints
├── dependencies.py  # Auth and permission checks
└── main.py          # App entry point
```

## Requirements

- Python 3.12+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./auth.db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPassword123!
ADMIN_NAME=Admin
```

## Running

```bash
python run.py
```

This creates the database, seeds initial data (permissions, admin role, admin user) and starts the server at `http://127.0.0.1:8000`.

API documentation available at `http://127.0.0.1:8000/docs`.

## Docker (optional)

```bash
docker compose up --build
```

## Tests

```bash
pytest tests/ -v
```

## Default admin credentials

- Email: `admin@example.com`
- Password: `AdminPassword123!`
