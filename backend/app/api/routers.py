from fastapi import APIRouter
from app.api.routes import houses, bookings

api_router = APIRouter(prefix="/api")

api_router.include_router(houses.router, tags=["houses"])
api_router.include_router(bookings.router, tags=["bookings"])