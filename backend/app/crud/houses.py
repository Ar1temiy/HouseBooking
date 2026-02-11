from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.houses import House
from app.schemas.houses import HouseCreate, HouseUpdate


async def get_houses(db: AsyncSession) -> list[House]:
    res = await db.execute(select(House).order_by(House.id))
    return list(res.scalars().all())


async def get_house_by_id(db: AsyncSession, house_id: int) -> House | None:
    res = await db.execute(select(House).where(House.id == house_id))
    return res.scalar_one_or_none()


async def create_house(db: AsyncSession, data: HouseCreate) -> House:
    house = House(**data.model_dump())
    db.add(house)
    await db.commit()
    await db.refresh(house)
    return house


async def update_house(db: AsyncSession, house: House, data: HouseUpdate) -> House:
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(house, k, v)

    await db.commit()
    await db.refresh(house)
    return house


async def delete_house(db: AsyncSession, house: House) -> None:
    await db.delete(house)
    await db.commit()
