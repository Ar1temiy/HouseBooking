from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.bookings import BookingCreate, BookingRead
from app.crud.bookings import (get_user_bookings,get_booking,create_booking,cancel_booking,get_all_bookings)
from app.models.bookings import Status

router = APIRouter(prefix="/bookings")

# Временно: вместо авторизации
DUMMY_USER_ID = 1


@router.get("/me", response_model=list[BookingRead])
async def my_bookings(db: AsyncSession = Depends(get_db)):
    return await get_user_bookings(db, user_id=DUMMY_USER_ID)


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking_endpoint(payload: BookingCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_booking(db, user_id=DUMMY_USER_ID, data=payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_my_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    booking = await get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != DUMMY_USER_ID:
        raise HTTPException(status_code=403, detail="Not your booking")

    return await cancel_booking(db, booking)


# Админская ручка (пока без авторизации)
@router.get("", response_model=list[BookingRead])
async def all_bookings(db: AsyncSession = Depends(get_db)):
    return await get_all_bookings(db)
