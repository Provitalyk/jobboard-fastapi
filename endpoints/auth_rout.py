import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jinja2 import FileSystemLoader, Environment
from auth import create_verification_token, verify_verification_token, verify_password, create_access_token
from services.user_service import UserService
from dependencies import get_user_service
from schemas import Token
from utils.email import send_verification_email


router = APIRouter(tags=["Аутентификация пользователя"])

# Настройка шаблонов
template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(template_dir))



@router.post("/login", summary="Аутентификация пользователя",
    description="Выполняет вход пользователя по email и паролю. "
                "Проверяет, что email и пароль корректны, а также что email подтверждён. "
                "В случае успеха возвращает JWT-токен.", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.get_user_by_email(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified. Check your email.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "name": user.name, "is_company": user.is_company}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/resend-verification-email",
    summary="Повторно отправить письмо подтверждения",
    description="Отправляет повторное письмо для подтверждения email на указанный адрес. "
                "Используется, если пользователь не получил письмо при регистрации. "
                "Доступно только для неподтверждённых учётных записей.",
    responses={
        200: {
            "description": "Письмо успешно отправлено",
            "content": {
                "application/json": {
                    "example": {"message": "Verification email sent"}
                }
            }
        },
        400: {
            "description": "Email уже подтверждён или пользователь не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already verified"}
                }
            }
        }
    }
)
async def resend_verification_email(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_email(email)
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    token = create_verification_token(email)
    send_verification_email(email, user.name, token)
    return {"message": "Verification email sent"}


@router.get("/verify-email",
    summary="Подтвердить email по токену",
    description="Активирует учётную запись пользователя по временному токену, "
                "отправленному на email. После подтверждения пользователь может входить в систему.",
    responses={
        200: {
            "description": "Email успешно подтверждён",
            "content": {
                "application/json": {
                    "example": {"message": "Email verified successfully"}
                }
            }
        },
        400: {
            "description": "Токен недействителен или истёк",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid or expired token"}
                }
            }
        }
    }
)
async def verify_email(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    email = verify_verification_token(token)
    await user_service.verify_user(email)
    return {"message": "Email verified successfully"}


