"""Authentication business logic."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.config import create_access_token, hash_password, verify_password
from app.models import Permission, RolePermissionLink, User, UserRoleLink


def get_user_scopes(session: Session, user_id) -> list[str]:
    """Fetch all permission names for a user through their roles."""
    role_ids = session.exec(
        select(UserRoleLink.role_id).where(UserRoleLink.user_id == user_id)
    ).all()
    if not role_ids:
        return []
    perm_ids = session.exec(
        select(RolePermissionLink.permission_id).where(
            RolePermissionLink.role_id.in_(role_ids)
        )
    ).all()
    if not perm_ids:
        return []
    permissions = session.exec(
        select(Permission.name).where(Permission.id.in_(perm_ids))
    ).all()
    return list(permissions)


def authenticate_user(session: Session, email: str, password: str) -> str:
    """Validate credentials and return a JWT token with scopes."""
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    scopes = get_user_scopes(session, user.id)
    return create_access_token(user.id, scopes)


def register_user(session: Session, name: str, email: str, password: str) -> User:
    """Create a new user. Raises 409 if email already exists."""
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(name=name, email=email, password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
