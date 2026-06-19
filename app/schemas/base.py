"""Base schema with shared validation logic."""

from pydantic import BaseModel, model_validator


class Base(BaseModel):
    """Base schema that strips whitespace from all string fields."""

    @model_validator(mode="before")
    @classmethod
    def strip_fields(cls, values):
        return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}
