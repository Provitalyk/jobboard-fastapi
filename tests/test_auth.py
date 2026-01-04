import pytest
from httpx import AsyncClient
from sqlalchemy import update
from models.user import users
from main import app
import uuid


def random_email():
    return f"user_{uuid.uuid4()}@test.com"


@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient):
    email = random_email()
    password = "correct123"

    # 1. Регистрация
    response = await client.post("/users/", json={
        "email": email,
        "name": f"User_{uuid.uuid4().hex[:6]}",
        "password": password,
        "is_company": False
    })
    assert response.status_code == 200, f"Регистрация не удалась: {response.json()}"

    # 2. Подтверждаем email вручную
    database = app.state.database
    query = update(users).where(users.c.email == email).values(is_verified=True)
    await database.execute(query)

    # 3. Попытка входа с неправильным паролем
    response = await client.post("/login", data={
        "username": email,
        "password": "wrong123"
    })

    # 4. Проверка
    assert response.status_code == 401, "Ожидался 401 при неверном пароле"
    assert response.json()["detail"] == "Incorrect email or password"