import pytest
from httpx import AsyncClient
import uuid


def random_email():
    return f"user_{uuid.uuid4()}@test.com"


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    email = random_email()

    response = await client.post("/users/", json={
        "email": email,
        "name": f"User_{uuid.uuid4().hex[:6]}",
        "password": "secret123",
        "is_company": False
    })
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["email"] == email
    assert "id" in data


@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient):
    email = random_email()
    name = f"User_{uuid.uuid4().hex[:6]}"

    # Первое создание
    response = await client.post("/users/", json={
        "email": email,
        "name": name,
        "password": "secret123",
        "is_company": False
    })
    assert response.status_code == 200

    # Второе — должно быть 400
    response = await client.post("/users/", json={
        "email": email,
        "name": f"Another_{uuid.uuid4().hex[:6]}",
        "password": "secret123",
        "is_company": False
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]