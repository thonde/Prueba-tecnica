"""User management endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.dependencies import PermissionChecker
from app.models import User
from app.schemas.assign import AssignRoleRequest
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/{user_id}/roles", status_code=204)
def assign_roles(
    user_id: uuid.UUID,
    data: AssignRoleRequest,
    current_user: Annotated[User, Depends(PermissionChecker("users:write"))],
    session: SessionDep,
):
    """Assign roles to a user. Requires users:write scope."""
    user_service.assign_roles(session, user_id, data.role_ids)
