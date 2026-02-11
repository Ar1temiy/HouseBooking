from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookings import Booking, Status


async def get_house_busy_ranges(
    db: AsyncSession,
    house_id: int,
    date_from: date,
    date_to: date,
) -> list[Booking]:
    """
    Возвращаем брони, которые пересекаются с заданным окном [date_from, date_to).
    date_to НЕ включительно.
    """
    stmt = (
        select(Booking)
        .where(
            and_(
                Booking.house_id == house_id,
                Booking.status != Status.cancelled,
                Booking.date_from < date_to,   # пересечение
                Booking.date_to > date_from,   # пересечение
            )
        )
        .order_by(Booking.date_from)
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())
