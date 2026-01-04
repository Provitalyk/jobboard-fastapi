from databases import Database
from db.base import database
from repositories.user_repository import UserRepository
from repositories.job_repository import JobRepository
from services.user_service import UserService
from services.job_service import JobService
from fastapi import Depends


async def get_database() -> Database:
    return database


def get_user_repository(db: Database = Depends(get_database)) -> UserRepository:
    return UserRepository(db)


def get_job_repository(db: Database = Depends(get_database)) -> JobRepository:
    return JobRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_job_service(repo: JobRepository = Depends(get_job_repository)) -> JobService:
    return JobService(repo)