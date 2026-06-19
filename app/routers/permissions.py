"""Permission management endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.dependencies import PermissionChecker, get_current_user
from app.models import User
from app.schemas.permission import PermissionRequest, PermissionResponse
from app.services import permission as permission_service

router = APIRouter(prefix="/permissions", tags=["Permissions"])
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[PermissionResponse])
def list_permissions(current_user: CurrentUser, session: SessionDep):
    """Retrieve all available permissions."""
    return permission_service.list_all(session)


@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: uuid.UUID, current_user: CurrentUser, session: SessionDep
):
    """Retrieve a single permission by its ID."""
    return permission_service.get_by_id(session, permission_id)


@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(
    data: PermissionRequest,
    current_user: Annotated[User, Depends(PermissionChecker("permissions:write"))],
    session: SessionDep,
):
    """Create a new permission. Requires permissions:write scope."""
    return permission_service.create(session, data.name, data.description)
