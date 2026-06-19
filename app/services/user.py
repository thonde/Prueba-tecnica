"""User business logic."""

from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Role, User, UserRoleLink


def assign_roles(session: Session, user_id: UUID, role_ids: list[UUID]) -> None:
    """Assign roles to a user. Skips duplicates."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for r_id in role_ids:
        role = session.get(Role, r_id)
        if not role:
            raise HTTPException(status_code=404, detail=f"Role {r_id} not found")
        existing = session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == user_id,
                UserRoleLink.role_id == r_id,
            )
        ).first()
        if not existing:
            session.add(UserRoleLink(user_id=user_id, role_id=r_id))
    session.commit()
