"""Assignment request schemas."""

import uuid

from pydantic import BaseModel


class AssignRoleRequest(BaseModel):
    """List of role IDs to assign to a user."""

    role_ids: list[uuid.UUID]


class AssignPermissionRequest(BaseModel):
    """List of permission IDs to assign to a role."""

    permission_ids: list[uuid.UUID]
