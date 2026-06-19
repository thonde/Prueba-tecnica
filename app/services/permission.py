"""Permission business logic."""

from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Permission


def list_all(session: Session) -> list[Permission]:
    """Return all permissions."""
    return session.exec(select(Permission)).all()


def get_by_id(session: Session, permission_id: UUID) -> Permission:
    """Return a permission by ID or raise 404."""
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


def create(session: Session, name: str, description: str | None) -> Permission:
    """Create a new permission. Raises 409 if name already exists."""
    existing = session.exec(select(Permission).where(Permission.name == name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Permission already exists")
    permission = Permission(name=name, description=description)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission
