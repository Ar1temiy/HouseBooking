from fastapi import FastAPI, Depends
import app.models  # noqa

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.api.routers import api_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router)



