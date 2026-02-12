from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.models  # noqa

from app.core.config import settings
from app.api.routers import api_router
from app.core.exceptions import AppError
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "auth",
        "description": "Регистрация и авторизация пользователей.",
    },
    {
        "name": "users",
        "description": "Операции над текущим пользователем.",
    },
    {
        "name": "houses",
        "description": "Публичная и административная работа с домами и их доступностью.",
    },
    {
        "name": "bookings",
        "description": "Создание, просмотр и управление бронированиями.",
    },
]

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "API для сервиса бронирования домов. "
        "Для защищённых эндпоинтов используйте Bearer-токен, "
        "полученный через `/api/auth/register` или `/api/auth/login`."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
