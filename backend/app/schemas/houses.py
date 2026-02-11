from pydantic import BaseModel, ConfigDict


from app.models.houses import Bathroom


class HouseBase(BaseModel):
    title: str
    description: str
    price: int
    bedrooms: int
    bathroom: Bathroom


class HouseCreate(HouseBase):
    pass


class HouseUpdate(BaseModel):
    title: str|None = None
    description: str|None = None
    price: int|None = None
    bedrooms: int|None = None
    bathroom: Bathroom|None = None


class HouseRead(HouseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int