import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
import app.models  # важно: чтобы модели зарегистрировались
from app.db.base import Base

from app.models.houses import House, Bathroom


def _bathroom_yes():
    """
    У тебя enum Bathroom мог называться по-разному (yes/no или Bath/NonBath и т.п.).
    Эта функция пытается выбрать вариант "есть ванная" максимально безопасно.
    """
    # 1) если есть Bathroom.yes
    if hasattr(Bathroom, "yes"):
        return Bathroom.yes
    # 2) если есть Bathroom.Bath
    if hasattr(Bathroom, "Bath"):
        return Bathroom.Bath
    # 3) если есть Bathroom.has / Bathroom.true и т.п. — редко, но вдруг
    for name in ("has", "true", "with_bath", "bath"):
        if hasattr(Bathroom, name):
            return getattr(Bathroom, name)

    # 4) fallback: первый элемент enum
    return list(Bathroom)[0]


HOUSES = [
    {
        "title": "Домик у озера",
        "description": "Уютный домик с видом на воду, рядом пирс и прогулочные тропы.",
        "price": 12000,
        "bedrooms": 2,
        "bathroom": "yes",
    },
    {
        "title": "Лесной A-Frame",
        "description": "Треугольный домик в лесу, панорамные окна и тишина.",
        "price": 15000,
        "bedrooms": 1,
        "bathroom": "no",
    },
    {
        "title": "Семейный коттедж",
        "description": "Просторный дом для семьи или компании, много воздуха и света.",
        "price": 20000,
        "bedrooms": 3,
        "bathroom": "yes",
    },
    {
        "title": "Домик-студия",
        "description": "Компактный формат для двоих, всё необходимое внутри.",
        "price": 9000,
        "bedrooms": 1,
        "bathroom": "no",
    },
    {
        "title": "Домик с террасой",
        "description": "Терраса для завтраков, вечером — огни и атмосфера.",
        "price": 13000,
        "bedrooms": 2,
        "bathroom": "yes",
    },
]


async def main():
    engine = create_async_engine(settings.DB_URL, echo=False)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    # Таблицы уже должны быть через alembic, но на всякий случай можно оставить это:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yes_val = _bathroom_yes()

    async with SessionLocal() as db:
        created = 0
        skipped = 0

        for item in HOUSES:
            title = item["title"]

            # Проверяем: есть ли уже дом с таким title
            res = await db.execute(select(House).where(House.title == title))
            existing = res.scalar_one_or_none()

            if existing:
                skipped += 1
                continue

            # bathroom: пробуем поставить enum "yes" безопасно
            house = House(
                title=item["title"],
                description=item["description"],
                price=item["price"],
                bedrooms=item["bedrooms"],
                bathroom=yes_val,  # enum
            )

            db.add(house)
            created += 1

        await db.commit()

    await engine.dispose()
    print(f"Seed done ✅ created={created}, skipped={skipped}")


if __name__ == "__main__":
    asyncio.run(main())
