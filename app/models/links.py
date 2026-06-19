import uuid

from sqlmodel import Field, SQLModel


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission_links"

    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: uuid.UUID = Field(foreign_key="permission.id", primary_key=True)


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"

    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)
