"""Permission request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import Base


class PermissionRequest(Base):
    """Payload for creating or updating a permission."""

    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=60)


class PermissionResponse(BaseModel):
    """Permission data returned in API responses."""

    id: UUID
    name: str
    description: str | None
    created_at: datetime
