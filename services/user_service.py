from repositories.user_repository import UserRepository
from schemas import User, UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> User:
        return await self.user_repository.create_user(user)

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repository.get_user_by_id(user_id)

    async def update_user(self, user_id: int, user: UserCreate) -> User:
        return await self.user_repository.update_user(user_id, user)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete_user(user_id)

    async def get_user_by_email(self, email: str) -> User:
        return await self.user_repository.get_user_by_email(email)