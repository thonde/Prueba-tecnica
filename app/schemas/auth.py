"""Authentication request and response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import Base


class AuthRequest(Base):
    """Login credentials: email and password."""

    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6, max_length=60)


class UserRequest(AuthRequest):
    """Registration payload: extends AuthRequest with a name field."""

    name: str = Field(..., min_length=1, max_length=50)


class UserResponse(BaseModel):
    """Public user data returned after registration."""

    id: uuid.UUID
    name: str
    email: str
    created_at: datetime


class AuthResponse(BaseModel):
    """JWT token response returned after successful login."""

    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    """Current authenticated user profile."""

    id: uuid.UUID
    name: str
    email: str
