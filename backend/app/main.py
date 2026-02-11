from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.models  # noqa

from app.core.config import settings
from app.api.routers import api_router
from app.core.exceptions import AppError

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
