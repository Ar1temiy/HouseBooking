import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Status(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"), nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    guests: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status, name="booking_status"),default=Status.pending,nullable=False)
    total_price: Mapped[int] = mapped_column(nullable=False)


