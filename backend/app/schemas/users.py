from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

from app.models.user import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None
    phone: str | None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    phone: str | None
    role: UserRole

class UserAdminUpdate(BaseModel):
    phone: str | None
    role: UserRole | None