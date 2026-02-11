import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, enum.Enum):
    client = "client"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False,)
    phone: Mapped[str | None] = mapped_column(String(32),unique=True,nullable=True,)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"),default=UserRole.client,nullable=False,)


