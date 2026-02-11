from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

import app.models.user     # noqa: F401
import app.models.houses   # noqa: F401
import app.models.bookings # noqa: F401