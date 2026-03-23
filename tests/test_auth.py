import pytest
from tests.conftest import get_token, auth_headers


def test_login_success(client, arrendador):
    response = client.post("/api/v1/auth/login", json={
        "email": "arrendador@test.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, arrendador):
    response = client.post("/api/v1/auth/login", json={
        "email": "arrendador@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "nobody@test.com",
        "password": "testpass123"
    })
    assert response.status_code == 401


def test_protected_route_no_token(client):
    response = client.get("/api/v1/contracts/me")
    assert response.status_code == 403


def test_protected_route_invalid_token(client):
    response = client.get("/api/v1/contracts/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 403
