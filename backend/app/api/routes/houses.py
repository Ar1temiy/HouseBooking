from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.houses import HouseCreate, HouseUpdate, HouseRead
from app.crud.houses import (get_houses,get_house_by_id,create_house,update_house,delete_house)

router = APIRouter(prefix="/houses")

@router.get("", response_model=list[HouseRead])
async def list_houses(db: AsyncSession = Depends(get_db)):
    return await get_houses(db)

@router.get("/{house_id}", response_model=HouseRead)
async def get_house(house_id: int, db: AsyncSession = Depends(get_db)):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@router.post("", response_model=HouseRead, status_code=status.HTTP_201_CREATED)
async def create_house_endpoint(payload: HouseCreate, db: AsyncSession = Depends(get_db)):
    return await create_house(db, payload)

@router.patch("/{house_id}", response_model=HouseRead)
async def update_house_endpoint(house_id: int, payload: HouseUpdate, db: AsyncSession = Depends(get_db)):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return await update_house(db, house, payload)

@router.delete("/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house_endpoint(house_id: int, db: AsyncSession = Depends(get_db)):
    house = await get_house_by_id(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    await delete_house(db, house)
    return None
