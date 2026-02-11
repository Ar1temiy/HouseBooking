from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta


from app.models.bookings import Booking, Status
from app.models.houses import House
from app.schemas.bookings import BookingCreate


async def get_user_bookings(db: AsyncSession, user_id: int) -> list[Booking]:
    res = await db.execute(
        select(Booking)
        .where(Booking.user_id == user_id)
        .order_by(Booking.id.desc())
    )
    return list(res.scalars().all())


async def has_overlap(db: AsyncSession, house_id: int, date_from: date, date_to: date) -> bool:
    # пересечение диапазонов: (start < existing_end) and (end > existing_start)
    stmt = select(Booking.id).where(
        and_(
            Booking.house_id == house_id,
            Booking.status != Status.cancelled,
            date_from < Booking.date_to,
            date_to > Booking.date_from,
        )
    )
    res = await db.execute(stmt)
    return res.first() is not None


async def create_booking(db: AsyncSession, user_id: int, data: BookingCreate) -> Booking:
    # 1) Проверяем, что дом существует
    house_res = await db.execute(select(House).where(House.id == data.house_id))
    house = house_res.scalar_one_or_none()
    if not house:
        raise ValueError("House not found")

    # 2) Считаем интервал дат
    # start_date включительно, date_to не включительно
    if data.days < 1:
        raise ValueError("days must be >= 1")

    date_from = data.start_date
    date_to = data.start_date + timedelta(days=data.days)

    # 3) Проверяем пересечения
    if await has_overlap(db, house_id=data.house_id, date_from=date_from, date_to=date_to):
        raise ValueError("House is already booked for these dates")

    # 4) Считаем стоимость на бэке
    total_price = house.price * data.days

    # 5) Создаём бронь
    booking = Booking(
        user_id=user_id,
        house_id=data.house_id,
        date_from=date_from,
        date_to=date_to,
        guests=data.guests,
        status=Status.pending,
        total_price=total_price,
    )

    # 6) Сохраняем в БД
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking


async def cancel_booking(db: AsyncSession, booking: Booking) -> Booking:
    booking.status = Status.cancelled
    await db.commit()
    await db.refresh(booking)
    return booking


async def get_booking(db: AsyncSession, booking_id: int) -> Booking | None:
    res = await db.execute(select(Booking).where(Booking.id == booking_id))
    return res.scalar_one_or_none()

async def get_all_bookings(db: AsyncSession) -> list[Booking]:
    res = await db.execute(select(Booking).order_by(Booking.id.desc()))
    return list(res.scalars().all())
