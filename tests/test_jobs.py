import uuid
import pytest
from httpx import AsyncClient


def random_email():
    return f"user_{uuid.uuid4()}@test.com"


@pytest.mark.anyio
async def test_create_job_unauthorized(client: AsyncClient):
    response = await client.post("/jobs/", json={
        "user_id": 999,
        "title": "Test Job",
        "description": "Test",
        "salary_from": 100000,
        "salary_to": 150000
    })
    assert response.status_code == 401