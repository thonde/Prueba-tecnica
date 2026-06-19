"""Seed script to preload default permissions, admin role and admin user."""

from sqlmodel import Session, SQLModel, select

from app.config import hash_password, settings
from app.db.database import engine
from app.models import (
    Permission,
    Role,
    RolePermissionLink,
    User,
    UserRoleLink,
)

DEFAULT_PERMISSIONS = [
    ("users:read", "Can read user information"),
    ("users:write", "Can create and modify users"),
    ("roles:read", "Can read roles"),
    ("roles:write", "Can create and modify roles"),
    ("permissions:read", "Can read permissions"),
    ("permissions:write", "Can create and modify permissions"),
]


def run() -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        permission: list[Permission] = []
        for name, description in DEFAULT_PERMISSIONS:
            perm = session.exec(
                select(Permission).where(Permission.name == name)
            ).first()
            if not perm:
                perm = Permission(name=name, description=description)
                session.add(perm)
            permission.append(perm)
        session.commit()
        for p in permission:
            session.refresh(p)

        admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
        if not admin_role:
            admin_role = Role(
                name="admin",
                description="Admin role",
            )
            session.add(admin_role)
            session.commit()
            session.refresh(admin_role)
        for perm in permission:
            link = session.exec(
                select(RolePermissionLink).where(
                    RolePermissionLink.role_id == admin_role.id,
                    RolePermissionLink.permission_id == perm.id,
                )
            ).first()
            if not link:
                session.add(
                    RolePermissionLink(role_id=admin_role.id, permission_id=perm.id)
                )
        session.commit()

        admin_user = session.exec(
            select(User).where(User.email == settings.ADMIN_EMAIL)
        ).first()
        if not admin_user:
            admin_user = User(
                name=settings.ADMIN_NAME,
                email=settings.ADMIN_EMAIL,
                password=hash_password(settings.ADMIN_PASSWORD),
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)

        user_role = session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == admin_user.id,
                UserRoleLink.role_id == admin_role.id,
            )
        ).first()
        if not user_role:
            session.add(UserRoleLink(user_id=admin_user.id, role_id=admin_role.id))
            session.commit()

        print("Precarga completada")


if __name__ == "__main__":
    import uvicorn

    run()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
