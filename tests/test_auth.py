"""Authentication endpoint tests."""


def test_login_success(client, admin_user):
    """Login with valid credentials returns a JWT token."""
    response = client.post(
        "/auth/login",
        json={"email": "admin@test.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, admin_user):
    """Login with wrong password returns 401."""
    response = client.post(
        "/auth/login",
        json={"email": "admin@test.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_register_duplicate_email(client, admin_user):
    """Register with an existing email returns 409."""
    response = client.post(
        "/auth/register",
        json={
            "email": "admin@test.com",
            "password": "Password123!",
            "name": "Duplicate",
        },
    )
    assert response.status_code == 409


def test_me_returns_user(client, auth_header):
    """GET /me with valid token returns user profile."""
    response = client.get("/auth/me", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["name"] == "Admin"


def test_create_role_requires_scope(client, basic_header):
    """Creating a role without roles:write scope returns 403."""
    response = client.post(
        "/roles",
        json={"name": "editor", "description": "Editor role"},
        headers=basic_header,
    )
    assert response.status_code == 403
