## Платформа для поиска работы:

- Компаниям публиковать вакансии
- Пользователям регистрироваться и искать работу
- Получать email-подтверждение при регистрации
- Безопасная аутентификация через JWT


## Функционал:

Бэкенд (FastAPI)
- Регистрация и авторизация с JWT
- Подтверждение email через письмо (в дальнейшем SMTP)
- Управление вакансиями: создание, просмотр
- Валидация данных (Pydantic), тестирование
- Асинхронная работа с SQLite (можно заменить на PostgreSQL)


| Слой                 | Технологии                                                            |
|----------------------|-----------------------------------------------------------------------|
| Бэкенд               | Python, FastAPI, SQLAlchemy, databases, PyJWT, passlib, pytest, anyio |
| БД                   | SQLite (тесты), PostgreSQL (в будущем)                                |
| Фронтенд (в будущем) | (React, JavaScript, Fetch API)                                        |
| Email (в будущем)    | SMTP (Gmail), Jinja2 (HTML-шаблоны)                                   |
| Тестирование         | pytest, httpx, AsyncClient                                            |



## Установка и запуск:

pip install -r requirements.txt

Настрой переменные окружения:

Создай файл `.env_dev`

DATABASE_URL="sqlite:///name_db"   (или "postgresql://postgres:postgres@localhost:5432/name_db")
SECRET_KEY=your-super-secret-test-key-change-in-prod 
ALGORITHM=HS256 
ACCESS_TOKEN_EXPIRE_MINUTES=30


Запуск:

uvicorn main:app --reload --host 127.0.0.1 --port 8000


## Тестирование:

pytest -v -s
- 100% покрытие основных сценариев
- Мок-БД, автоматическая очистка
- Подтверждение email в тестах



## Примеры запросов

### Регистрация 
(Создаёт нового пользователя и отправляет письмо для подтверждения email)

POST http://127.0.0.1:8000/users/
Content-Type: application/json

{
  "email": "alice@example.com",
  "name": "Alice",
  "password": "secret123",
  "is_company": false
}

Ответ: 

{
  "id": 1,
  "email": "alice@example.com",
  "name": "Alice",
  "is_company": false,
  "is_verified": false
}

На email приходит письмо со ссылкой:
http://127.0.0.1:8000/auth/verify-email?token=xxx

### Логин и получение JWT
(Получает токен доступа после успешной аутентификации. Пароль хранится в зашифрованном виде)

POST http://127.0.0.1:8000/login
Content-Type: application/x-www-form-urlencoded
username=alice@example.com&password=secret123

Ответ: 

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx",
  "token_type": "bearer"
}

### Подтверждение email
(Активирует аккаунт пользователя)

GET http://127.0.0.1:8000/auth/verify-email?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

Ответ:

{
  "message": "Email успешно подтверждён"
}

### Повторная отправка письма
(Отправляет письмо повторно, если email не подтверждён)

POST http://127.0.0.1:8000/resend-verification-email
Content-Type: application/json

{
  "email": "alice@example.com"
}

Ответ: 

{
  "message": "Verification email sent"
}

Если email уже подтверждён:

{ "detail": "Email already verified" }


### Создание вакансии
(Доступно только авторизованным пользователям)

POST http://127.0.0.1:8000/jobs/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
Content-Type: application/json

{
  "user_id": 1,
  "title": "Middle Python Developer",
  "description": "Ищем опытного разработчика на FastAPI и SQLAlchemy",
  "salary_from": 120000,
  "salary_to": 180000
}

Ответ: 

{
  "id": 1,
  "user_id": 1,
  "title": "Middle Python Developer",
  "description": "Ищем опытного разработчика на FastAPI и SQLAlchemy",
  "salary_from": 120000,
  "salary_to": 180000,
  "created_at": "2025-04-05T10:00:00Z"
}

### Получение всех вакансий
(Публичный маршрут — не требует авторизации)

GET http://127.0.0.1:8000/jobs/

Ответ: 

[
  {
    "id": 1,
    "user_id": 1,
    "title": "Middle Python Developer",
    "description": "Ищем опытного разработчика на FastAPI и SQLAlchemy",
    "salary_from": 120000,
    "salary_to": 180000,
    "created_at": "2025-04-05T10:00:00Z"
  }
]

### Получение профиля пользователя
(Доступно только авторизованным пользователям. Возвращает текущего пользователя)

GET http://127.0.0.1:8000/users/me
Authorization: Bearer <access_token>

Ответ: 

{
  "id": 1,
  "email": "alice@example.com",
  "name": "Alice",
  "is_company": false,
  "is_verified": true
}

### Обновление профиля

PUT http://127.0.0.1:8000/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Alice Smith",
  "is_company": true
}

Ответ: 

{
  "id": 1,
  "email": "alice@example.com",
  "name": "Alice Smith",
  "is_company": true,
  "is_verified": true
}









