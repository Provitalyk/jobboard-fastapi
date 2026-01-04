from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from schemas import UserCreate, User
from services.user_service import UserService
from dependencies import get_user_service


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/", summary="Создать нового пользователя",
             description="Регистрирует нового пользователя в системе. Проверяет уникальность email и имени. ""Если email или имя уже заняты — возвращается ошибка 400.",
             response_model=User, responses={
    400: {
        "description": "Email or name already registered",
        "content": {
            "application/json": {
                "example": {"detail": "Email or name already registered"}
            }
        }
    }
})
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        created_user = await service.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", summary="Получить список всех пользователей",
    description="Возвращает список всех зарегистрированных пользователей. "
                "Данные отсортированы по дате регистрации (от новых к старым).", response_model=list[User])
async def read_users(service: UserService = Depends(get_user_service)):
    return await service.get_all_users()


@router.get("/{user_id}", summary="Получить пользователя по ID",
    description="Возвращает данные пользователя по указанному идентификатору. "
                "Если пользователь не найден — возвращается ошибка 404.", response_model=User)
async def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}", summary="Обновить данные пользователя",
    description="Изменяет данные существующего пользователя. Проверяет, что email или имя не заняты. "
                "Если пользователь не найден или нарушены ограничения — возвращается ошибка 400.", response_model=User)
async def update_user(
    user_id: int,
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", summary="Удалить пользователя",
    description="Удаляет пользователя по указанному ID. "
                "Если пользователь не найден или произошла ошибка — возвращается сообщение об ошибке.", response_model=dict)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.delete_user(user_id)
        return {"message": f"User with ID {user_id} has been deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))