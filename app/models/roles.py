import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, max_length=50)
    description: str = Field(nullable=False, max_length=60)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
