from db.base import database, metadata, engine
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from endpoints import jobs, users, auth_rout
from schemas import Token
from dependencies import get_user_service
from services.user_service import UserService
from auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Подключено к базе данных")
    metadata.create_all(bind=engine)
    await database.connect()
    app.state.database = database

    yield

    print("Отключено от базы данных")
    await database.disconnect()


app = FastAPI(lifespan=lifespan, summary="Биржа труда", debug=True)


app.include_router(users.router)
app.include_router(auth_rout.router)
app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "Биржа труда"}


@app.post("/login", summary="Получение токена", description="Для авторизации", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    # Ищем пользователя
    try:
        user = await user_service.get_user_by_email(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "is_company": user.is_company
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

