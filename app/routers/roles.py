"""Role management endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.dependencies import PermissionChecker, get_current_user
from app.models import User
from app.schemas.assign import AssignPermissionRequest
from app.schemas.role import RoleRequest, RoleResponse
from app.services import role as role_service

router = APIRouter(prefix="/roles", tags=["Roles"])
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[RoleResponse])
def list_roles(current_user: CurrentUser, session: SessionDep):
    """Retrieve all available roles."""
    return role_service.list_all(session)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: uuid.UUID, current_user: CurrentUser, session: SessionDep):
    """Retrieve a single role by its ID."""
    return role_service.get_by_id(session, role_id)


@router.post("", response_model=RoleResponse, status_code=201)
def create_role(
    data: RoleRequest,
    current_user: Annotated[User, Depends(PermissionChecker("roles:write"))],
    session: SessionDep,
):
    """Create a new role. Requires roles:write scope."""
    return role_service.create(session, data.name, data.description)


@router.post("/{role_id}/permissions", status_code=204)
def assign_permissions(
    role_id: uuid.UUID,
    data: AssignPermissionRequest,
    current_user: Annotated[User, Depends(PermissionChecker("roles:write"))],
    session: SessionDep,
):
    """Assign permissions to a role. Requires roles:write scope."""
    role_service.assign_permissions(session, role_id, data.permission_ids)
