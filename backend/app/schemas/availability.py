from datetime import date
from pydantic import BaseModel, ConfigDict


class BusyRange(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date_from: date
    date_to: date
