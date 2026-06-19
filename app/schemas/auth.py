"""Authentication request and response schemas."""

import re
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.base import Base


class AuthRequest(Base):
    """Login credentials: email and password."""

    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., examples=["SecurePass123!"])


class UserRequest(AuthRequest):
    """Registration payload: extends AuthRequest with a name field."""

    name: str = Field(..., min_length=1, max_length=50, examples=["John Doe"])
    password: str = Field(
        ..., min_length=8, max_length=60, examples=["SecurePass123!"]
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Must contain at least one special character")
        return v


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
