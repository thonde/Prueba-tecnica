"""Role request and response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.base import Base


class RoleRequest(Base):
    """Payload for creating or updating a role."""

    name: str = Field(..., min_length=1, max_length=50, examples=["editor"])
    description: str | None = Field(None, max_length=60, examples=["Editor role"])


class RoleResponse(BaseModel):
    """Role data returned in API responses."""

    id: uuid.UUID
    name: str
    description: str | None
    created_at: datetime
