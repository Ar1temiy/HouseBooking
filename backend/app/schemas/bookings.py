from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from app.models.bookings import Status


class BookingBase(BaseModel):
    house_id: int
    date_from: date
    date_to: date
    guests: int
    total_price: int


class BookingCreate(BaseModel):
    house_id: int
    start_date: date
    days: int = Field(..., ge=1)
    guests: int = Field(..., ge=1)

class BookingUpdate(BaseModel):
    status: Status

class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    house_id: int
    date_from: date
    date_to: date
    guests: int
    status: Status
    total_price: int
