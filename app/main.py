"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from run import run as seed

from app.db.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.permissions import router as permissions_router
from app.routers.roles import router as roles_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed()
    yield


app = FastAPI(
    title="Auth API",
    description="API de Autenticación y Autorización con FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)


@app.get("/")
def read_root():
    return {"message": "API de Autenticación y Autorización corriendo"}
