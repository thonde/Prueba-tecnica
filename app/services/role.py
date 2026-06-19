"""Role business logic."""

from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Permission, Role, RolePermissionLink


def list_all(session: Session) -> list[Role]:
    """Return all roles."""
    return session.exec(select(Role)).all()


def get_by_id(session: Session, role_id: UUID) -> Role:
    """Return a role by ID or raise 404."""
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def create(session: Session, name: str, description: str | None) -> Role:
    """Create a new role. Raises 409 if name already exists."""
    existing = session.exec(select(Role).where(Role.name == name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Role already exists")
    role = Role(name=name, description=description)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def assign_permissions(
    session: Session, role_id: UUID, permission_ids: list[UUID]
) -> None:
    """Assign permissions to a role. Skips duplicates."""
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    for perm_id in permission_ids:
        permission = session.get(Permission, perm_id)
        if not permission:
            raise HTTPException(
                status_code=404, detail=f"Permission {perm_id} not found"
            )
        existing = session.exec(
            select(RolePermissionLink).where(
                RolePermissionLink.role_id == role_id,
                RolePermissionLink.permission_id == perm_id,
            )
        ).first()
        if not existing:
            session.add(RolePermissionLink(role_id=role_id, permission_id=perm_id))
    session.commit()
