
pytest_plugins = ["anyio"]

import pytest
import os
import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from databases import Database
from main import app
from db.base import metadata


# Уникальное имя файла БД для каждого запуска
TEST_DB_FILE = f"test_{uuid.uuid4().hex}.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{TEST_DB_FILE}"
SYNC_DATABASE_URL = f"sqlite:///./{TEST_DB_FILE}"

engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
database = Database(DATABASE_URL)


@pytest.fixture(autouse=True, scope="function")
async def setup_database():
    # Удаляем старую БД, если осталась
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except:
            await asyncio.sleep(0.1)
            try:
                os.remove(TEST_DB_FILE)
            except:
                pass

    # Создаём таблицы
    metadata.create_all(engine)

    # Подключаемся к БД
    await database.connect()
    app.state.database = database

    yield

    # Отключаемся
    if database.is_connected:
        await database.disconnect()

    # Удаляем файл
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except:
            pass


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac