from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import NotFoundError, ConflictError
from datetime import date
from fastapi import Query

from app.schemas.availability import BusyRange
from app.crud.availability import get_house_busy_ranges

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.houses import HouseCreate, HouseUpdate, HouseRead
from app.crud.houses import (get_houses, get_house_by_id, create_house, update_house, delete_house)

router = APIRouter(prefix="/houses", tags=["houses"])
# -------- PUBLIC (доступно всем) --------

@router.get(
    "",
    response_model=list[HouseRead],
    summary="Список домов",
    description="Возвращает список всех доступных домов.",
)
async def list_houses(db: AsyncSession = Depends(get_db)):
    return await get_houses(db)


@router.get(
    "/{house_id}",
    response_model=HouseRead,
    summary="Дом по ID",
    description="Возвращает информацию о конкретном доме.",
    responses={404: {"description": "Дом не найден"}},
)
async def get_house(house_id: int, db: AsyncSession = Depends(get_db)):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise NotFoundError("House not found")
    return house


# -------- ADMIN ONLY --------

@router.post(
    "",
    response_model=HouseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать дом (admin)",
    description="Создаёт новый дом. Доступно только администратору.",
    responses={403: {"description": "Только для администратора"}},
)
async def create_house_endpoint(payload: HouseCreate, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    return await create_house(db, payload)


@router.patch(
    "/{house_id}",
    response_model=HouseRead,
    summary="Обновить дом (admin)",
    description="Частично обновляет данные дома. Доступно только администратору.",
    responses={403: {"description": "Только для администратора"}, 404: {"description": "Дом не найден"}},
)
async def update_house_endpoint(
    house_id: int,
    payload: HouseUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise NotFoundError("House not found")
    return await update_house(db, house, payload)

@router.get(
    "/{house_id}/availability",
    response_model=list[BusyRange],
    summary="Занятые интервалы дома",
    description="Возвращает интервалы занятости дома в диапазоне `[date_from, date_to)`.",
    responses={400: {"description": "Некорректный диапазон дат"}, 404: {"description": "Дом не найден"}},
)
async def house_availability(
    house_id: int,
    date_from: date = Query(..., description="Start date (inclusive)"),
    date_to: date = Query(..., description="End date (exclusive)"),
    db: AsyncSession = Depends(get_db),
):
    # 1) базовая валидация
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="date_from must be < date_to")

    # 2) проверим, что дом существует (чтобы не возвращать пустоту на неправильный id)
    house = await get_house_by_id(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # 3) достаём брони и отдаём только интервалы
    bookings = await get_house_busy_ranges(db, house_id, date_from, date_to)
    return [BusyRange(date_from=b.date_from, date_to=b.date_to) for b in bookings]

@router.delete(
    "/{house_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить дом (admin)",
    description="Удаляет дом. Если есть связанные бронирования — возвращает ошибку.",
    responses={403: {"description": "Только для администратора"}, 404: {"description": "Дом не найден"}, 409: {"description": "Есть связанные бронирования"}},
)
async def delete_house_endpoint(
    house_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise NotFoundError("House not found")

    try:
        await delete_house(db, house)
    except IntegrityError:
        await db.rollback()
        raise ConflictError("Нельзя удалить дом: есть связанные бронирования")

    return None