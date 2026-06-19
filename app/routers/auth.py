"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.dependencies import get_current_user
from app.models import User
from app.schemas.auth import (
    AuthRequest,
    AuthResponse,
    MeResponse,
    UserRequest,
    UserResponse,
)
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/login", response_model=AuthResponse)
def login(data: AuthRequest, session: SessionDep):
    """Authenticate a user and return a JWT access token with scopes."""
    token = auth_service.authenticate_user(session, data.email, data.password)
    return AuthResponse(access_token=token)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserRequest, session: SessionDep):
    """Register a new user. Public endpoint."""
    user = auth_service.register_user(session, data.name, data.email, data.password)
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )


@router.get("/me", response_model=MeResponse)
def me(current_user: CurrentUser):
    """Return the currently authenticated user's profile."""
    return MeResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
    )
