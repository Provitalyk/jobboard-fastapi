from repositories.job_repository import JobRepository
from schemas import Job, JobCreate


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def create_job(self, job: JobCreate) -> Job:
        return await self.job_repository.create_job(job)

    async def get_all_jobs(self) -> list[Job]:
        return await self.job_repository.get_all_jobs()

    async def get_job_by_id(self, job_id: int) -> Job:
        return await self.job_repository.get_job_by_id(job_id)

    async def update_job(self, job_id: int, job: JobCreate) -> Job:
        return await self.job_repository.update_job(job_id, job)

    async def delete_job(self, job_id: int) -> bool:
        return await self.job_repository.delete_job(job_id)