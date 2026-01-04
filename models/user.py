from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from db.base import metadata
from datetime import datetime, timezone

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True),
    Column("name", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_company", Boolean, default=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
    Column("updated_at", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
)