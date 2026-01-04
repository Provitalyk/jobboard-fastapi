from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user
from schemas import JobCreate, Job, User
from services.job_service import JobService
from dependencies import get_job_service

router = APIRouter(prefix="/jobs", tags=["Вакансии"])

@router.post("/", summary="Создать новую вакансию",
    description="Создаёт новую вакансию. Проверяет, что пользователь с указанным user_id существует, "
                "и что значение 'salary_from' не превышает 'salary_to'. "
                "Возвращает созданную вакансию.", response_model=Job)
async def create_job(
    job: JobCreate,
    service: JobService = Depends(get_job_service),
    current_user: User = Depends(get_current_user)
):
    # Только авторизованные пользователи
    if job.user_id != current_user.id and not current_user.is_company:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    try:
        return await service.create_job(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", summary="Получить список всех вакансий",
    description="Возвращает список всех активных и неактивных вакансий, отсортированных по дате создания — сначала новые. "
                "Если вакансий нет — возвращается пустой список.", response_model=list[Job])
async def read_jobs(service: JobService = Depends(get_job_service)):
    return await service.get_all_jobs()


@router.get("/{job_id}", summary="Получить вакансию по ID",
    description="Возвращает данные вакансии по указанному идентификатору. "
                "Если вакансия не найдена — возвращается ошибка 404.", response_model=Job)
async def read_job(
    job_id: int,
    service: JobService = Depends(get_job_service)
):
    try:
        return await service.get_job_by_id(job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{job_id}", summary="Обновить данные вакансии",
    description="Изменяет существующую вакансию. Проверяет, что пользователь (user_id) существует "
                "и что значение 'salary_from' не больше 'salary_to'. "
                "Если вакансия или пользователь не найдены — возвращается ошибка 400.", response_model=Job)
async def update_job(
    job_id: int,
    job: JobCreate,
    service: JobService = Depends(get_job_service)
):
    try:
        return await service.update_job(job_id, job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_id}", summary="Удалить вакансию",
    description="Удаляет вакансию по указанному ID. "
                "Если вакансия не найдена — возвращается ошибка 404.", response_model=dict)
async def delete_job(
    job_id: int,
    service: JobService = Depends(get_job_service)
):
    try:
        await service.delete_job(job_id)
        return {"message": f"Job with ID {job_id} has been deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))