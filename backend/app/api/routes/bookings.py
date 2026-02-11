from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError, ForbiddenError
from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.bookings import Status
from app.models.user import User
from app.schemas.bookings import BookingCreate, BookingRead
from app.crud.bookings import (get_user_bookings, get_booking, create_booking, cancel_booking, get_all_bookings)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/me", response_model=list[BookingRead])
async def my_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_user_bookings(db, user_id=current_user.id)


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking_endpoint(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_booking(db, user_id=current_user.id, data=payload)



@router.patch("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_my_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = await get_booking(db, booking_id)
    if not booking:
        raise NotFoundError("Booking not found")

    # запрещаем отменять чужую бронь
    if booking.user_id != current_user.id:
        raise ForbiddenError("Not your booking")

    # если уже отменено — можно вернуть как есть или 400 (тут вернём как есть)
    if booking.status == Status.cancelled:
        return booking

    return await cancel_booking(db, booking)


# -------------------- ADMIN --------------------

@router.get("/all", response_model=list[BookingRead])
async def all_bookings(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return await get_all_bookings(db)


@router.patch("/{booking_id}/confirm", response_model=BookingRead)
async def confirm_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    booking = await get_booking(db, booking_id)
    if not booking:
        raise NotFoundError("Booking not found")

    booking.status = Status.confirmed
    await db.commit()
    await db.refresh(booking)
    return booking


@router.patch("/{booking_id}/admin-cancel", response_model=BookingRead)
async def admin_cancel_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    booking = await get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    booking.status = Status.cancelled
    await db.commit()
    await db.refresh(booking)
    return booking
