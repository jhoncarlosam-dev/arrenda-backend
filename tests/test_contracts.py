import pytest
from tests.conftest import get_token, auth_headers


CONTRACT_PAYLOAD = {
    "arrendatario_id": None,  # set in tests
    "direccion": "Calle 123 # 45-67",
    "tipo": "Residencial",
    "valor": "1500000.00",
    "servicios": "Agua, Luz",
    "clausulas_opcionales": None,
}


def test_arrendador_can_create_contract(client, arrendador, arrendatario):
    token = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    response = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token))
    assert response.status_code == 201
    data = response.json()
    assert data["arrendador_id"] == arrendador.id
    assert data["arrendatario_id"] == arrendatario.id


def test_arrendatario_cannot_create_contract(client, arrendador, arrendatario):
    token = get_token(client, "arrendatario@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    response = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token))
    assert response.status_code == 403


def test_read_own_contract(client, arrendador, arrendatario):
    # Create contract as arrendador
    token_a = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    contract_id = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token_a)).json()["id"]

    # Arrendador can read it
    response = client.get(f"/api/v1/contracts/{contract_id}", headers=auth_headers(token_a))
    assert response.status_code == 200

    # Arrendatario can also read it
    token_t = get_token(client, "arrendatario@test.com", "testpass123")
    response = client.get(f"/api/v1/contracts/{contract_id}", headers=auth_headers(token_t))
    assert response.status_code == 200


def test_cannot_read_other_users_contract(client, arrendador, arrendatario, db):
    from app.services.user_service import create_user
    from app.schemas.user import UserCreate
    from app.models.user import RoleEnum

    other = create_user(db, UserCreate(
        nombre="Other User",
        email="other@test.com",
        password="testpass123",
        role=RoleEnum.ARRENDADOR,
    ))

    token_a = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    contract_id = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token_a)).json()["id"]

    # Other arrendador cannot read it
    other_token = get_token(client, "other@test.com", "testpass123")
    response = client.get(f"/api/v1/contracts/{contract_id}", headers=auth_headers(other_token))
    assert response.status_code == 403


def test_list_my_contracts(client, arrendador, arrendatario):
    token = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token))
    client.post("/api/v1/contracts/", json={**payload, "direccion": "Otra Dir"}, headers=auth_headers(token))

    response = client.get("/api/v1/contracts/me", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_own_contract(client, arrendador, arrendatario):
    token = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    contract_id = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token)).json()["id"]

    response = client.put(
        f"/api/v1/contracts/{contract_id}",
        json={"direccion": "Nueva Dirección 456"},
        headers=auth_headers(token)
    )
    assert response.status_code == 200
    assert response.json()["direccion"] == "Nueva Dirección 456"


def test_delete_own_contract(client, arrendador, arrendatario):
    token = get_token(client, "arrendador@test.com", "testpass123")
    payload = {**CONTRACT_PAYLOAD, "arrendatario_id": arrendatario.id}
    contract_id = client.post("/api/v1/contracts/", json=payload, headers=auth_headers(token)).json()["id"]

    response = client.delete(f"/api/v1/contracts/{contract_id}", headers=auth_headers(token))
    assert response.status_code == 204

    response = client.get(f"/api/v1/contracts/{contract_id}", headers=auth_headers(token))
    assert response.status_code == 404
