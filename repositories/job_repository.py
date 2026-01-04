from databases import Database
from models import jobs
from models.user import users
from schemas import JobCreate, Job
from datetime import datetime, timezone


class JobRepository:
    def __init__(self, database: Database):
        self.database = database

    async def create_job(self, job: JobCreate):
        # Проверка существования пользователя
        query = users.select().where(users.c.id == job.user_id)
        user = await self.database.fetch_one(query)
        if not user:
            raise ValueError("User not found")

        # Проверка зарплаты
        if job.salary_from > job.salary_to:
            raise ValueError("salary_from cannot be greater than salary_to")

        # Создание вакансии
        insert_query = jobs.insert().values(
            user_id=job.user_id,
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active or True,
        )
        last_record_id = await self.database.execute(insert_query)
        return await self.get_job_by_id(last_record_id)

    async def get_all_jobs(self):
        query = jobs.select().order_by(jobs.c.created_at.desc())
        rows = await self.database.fetch_all(query)
        return [Job(**dict(row)) for row in rows]

    async def get_job_by_id(self, job_id: int):
        query = jobs.select().where(jobs.c.id == job_id)
        row = await self.database.fetch_one(query)
        if not row:
            raise ValueError("Job not found")
        return Job(**dict(row))

    async def update_job(self, job_id: int, job: JobCreate):
        # Проверка существования вакансии
        await self.get_job_by_id(job_id)

        # Проверка пользователя
        query = users.select().where(users.c.id == job.user_id)
        user = await self.database.fetch_one(query)
        if not user:
            raise ValueError("User not found")

        # Проверка зарплаты
        if job.salary_from > job.salary_to:
            raise ValueError("salary_from cannot be greater than salary_to")

        # Обновление
        query = jobs.update().where(jobs.c.id == job_id).values(
            user_id=job.user_id,
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active,
            updated_at=datetime.now(timezone.utc)
        )
        await self.database.execute(query)
        return await self.get_job_by_id(job_id)

    async def delete_job(self, job_id: int):
        await self.get_job_by_id(job_id)
        query = jobs.delete().where(jobs.c.id == job_id)
        await self.database.execute(query)
        return True