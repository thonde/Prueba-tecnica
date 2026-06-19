"""Assignment request schemas."""

import uuid

from pydantic import BaseModel, Field


class AssignRoleRequest(BaseModel):
    """List of role IDs to assign to a user."""

    role_ids: list[uuid.UUID] = Field(
        ..., examples=[["550e8400-e29b-41d4-a716-446655440000"]]
    )


class AssignPermissionRequest(BaseModel):
    """List of permission IDs to assign to a role."""

    permission_ids: list[uuid.UUID] = Field(
        ..., examples=[["550e8400-e29b-41d4-a716-446655440000"]]
    )
