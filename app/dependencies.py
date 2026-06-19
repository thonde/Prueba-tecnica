"""Shared FastAPI dependencies for authentication and authorization."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlmodel import Session, select

from app.config import decode_access_token
from app.db.database import get_session
from app.models import User

security = HTTPBearer(
    description="JWT access token required. Use /auth/login to obtain one."
)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """Extract and validate JWT token, then return the authenticated user."""
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = UUID(user_id)
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user._scopes = payload.get("scopes", [])
    return user


class PermissionChecker:
    """Dependency that verifies the current user has a required scope."""

    def __init__(self, required_scope: str):
        self.required_scope = required_scope

    def __call__(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if self.required_scope not in getattr(current_user, "_scopes", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
