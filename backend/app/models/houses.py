import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Bathroom(str, enum.Enum):
    yes = "yes"
    no = "no"


class House(Base):
    __tablename__ = "houses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    bedrooms: Mapped[int] = mapped_column(nullable=False)
    bathroom: Mapped[Bathroom] = mapped_column(Enum(Bathroom, name="bathroom_type"),nullable=False,default=Bathroom.yes)


