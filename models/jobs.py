from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from db.base import metadata
from datetime import datetime, timezone

jobs = Table(
    "jobs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("title", String, index=True),
    Column("description", Text),
    Column("salary_from", Integer),
    Column("salary_to", Integer),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
    Column("updated_at", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
)