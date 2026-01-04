from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: str = Field(..., min_length=5)
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=6)
    is_company: Optional[bool] = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "user@example.com",
                    "name": "JohnDoe",
                    "password": "secret123",
                    "is_company": False
                }
            ]
        }
    )


class User(UserCreate):
    id: int
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "name": "JohnDoe",
                    "is_company": False,
                    "is_verified": True,
                    "created_at": "2025-04-05T12:00:00Z",
                    "updated_at": "2025-04-05T12:00:00Z"
                }
            ]
        }
    )


class JobCreate(BaseModel):
    user_id: int
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_id": 1,
                    "title": "Python Dev",
                    "description": "Write FastAPI code",
                    "salary_from": 100000,
                    "salary_to": 150000,
                    "is_active": True
                }
            ]
        }
    )


class Job(JobCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "title": "Python Dev",
                    "description": "Write FastAPI code",
                    "salary_from": 100000,
                    "salary_to": 150000,
                    "is_active": True,
                    "created_at": "2025-04-05T12:00:00Z",
                    "updated_at": "2025-04-05T12:00:00Z"
                }
            ]
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIs...",
                    "token_type": "bearer"
                }
            ]
        }
    )