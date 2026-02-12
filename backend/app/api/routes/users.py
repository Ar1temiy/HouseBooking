from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.users import UserRead
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/me",
    response_model=UserRead,
    summary="Профиль текущего пользователя",
    description="Возвращает данные пользователя из JWT токена.",
    responses={401: {"description": "Пользователь не авторизован"}},
)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
