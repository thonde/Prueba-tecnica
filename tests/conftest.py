"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.config import create_access_token, hash_password
from app.db.database import get_session
from app.main import app
from app.models import (
    Permission,
    Role,
    RolePermissionLink,
    User,
    UserRoleLink,
)

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(session):
    """Create an admin user with all default permissions."""
    user = User(
        name="Admin",
        email="admin@test.com",
        password=hash_password("password123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    role = Role(name="admin", description="Admin role")
    session.add(role)
    session.commit()
    session.refresh(role)

    scopes = ["users:read", "users:write", "roles:write", "permissions:write"]
    for scope in scopes:
        perm = Permission(name=scope, description=scope)
        session.add(perm)
        session.commit()
        session.refresh(perm)
        session.add(RolePermissionLink(role_id=role.id, permission_id=perm.id))
    session.commit()

    session.add(UserRoleLink(user_id=user.id, role_id=role.id))
    session.commit()

    return user


@pytest.fixture
def auth_header(admin_user, session):
    """Token with all admin scopes."""
    from app.services.auth import get_user_scopes

    scopes = get_user_scopes(session, admin_user.id)
    token = create_access_token(admin_user.id, scopes)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def basic_user(session):
    """A user with no roles or permissions."""
    user = User(
        name="Basic",
        email="basic@test.com",
        password=hash_password("password123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def basic_header(basic_user):
    """Token with no scopes."""
    token = create_access_token(basic_user.id, [])
    return {"Authorization": f"Bearer {token}"}
