from databases import Database
from models.user import users
from schemas import UserCreate, User
from datetime import datetime, timezone
from auth import get_password_hash


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    async def create_user(self, user: UserCreate):
        # Проверка уникальности email и name
        query = users.select().where(
            (users.c.email == user.email) | (users.c.name == user.name)
        )
        existing_user = await self.database.fetch_one(query)
        if existing_user:
            raise ValueError("Email or name already registered")

        # Вставляем нового пользователя
        insert_query = users.insert().values(
            email=user.email,
            name=user.name,
            hashed_password=get_password_hash(user.password),
            is_company=user.is_company,
            is_verified=False,
        )
        last_record_id = await self.database.execute(insert_query)

        # Возвращаем созданного пользователя
        return User(
            id=last_record_id,
            **user.model_dump(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    async def get_all_users(self):
        query = users.select()
        rows = await self.database.fetch_all(query)
        return [User(**dict(row)) for row in rows]

    async def get_user_by_id(self, user_id: int):
        query = users.select().where(users.c.id == user_id)
        row = await self.database.fetch_one(query)
        if not row:
            raise ValueError("User not found")
        return User(**dict(row))

    async def update_user(self, user_id: int, user: UserCreate):
        # Проверяем существование
        await self.get_user_by_id(user_id)

        # Проверка уникальности (кроме текущего пользователя)
        query = users.select().where(
            (users.c.id != user_id) &
            ((users.c.email == user.email) | (users.c.name == user.name))
        )
        conflict = await self.database.fetch_one(query)
        if conflict:
            raise ValueError("Email or name already in use")

        # Обновляем пользователя
        query = users.update().where(users.c.id == user_id).values(
            email=user.email,
            name=user.name,
            hashed_password=user.password,
            is_company=user.is_company,
            updated_at=datetime.now(timezone.utc)
        )
        await self.database.execute(query)
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: int):
        # Проверка наличия активных вакансий
        from models import jobs
        job_query = jobs.select().where(jobs.c.user_id == user_id).where(jobs.c.is_active == True)
        active_jobs = await self.database.fetch_all(job_query)
        if active_jobs:
            raise ValueError("Cannot delete user with active jobs")

        # Удаляем
        query = users.delete().where(users.c.id == user_id)
        await self.database.execute(query)
        return True

    async def get_user_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        row = await self.database.fetch_one(query)
        if not row:
            raise ValueError("User not found")
        return User(**dict(row))