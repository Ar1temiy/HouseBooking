from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictError, BadRequestError
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, TokenResponse
from app.crud.users import get_user_by_email
from app.models.user import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="Создаёт пользователя с ролью `client` и возвращает JWT access token.",
    responses={409: {"description": "Email уже зарегистрирован"}},
)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise ConflictError("Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        role=UserRole.client,
        hashed_password=hash_password(payload.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Авторизация пользователя",
    description=(
        "Проверяет email/пароль и возвращает JWT access token. "
        "В поле `username` формы передаётся email."
    ),
    responses={400: {"description": "Неверный email или пароль"}},
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # В OAuth2PasswordRequestForm поле называется username,
    # но мы используем его как email.
    user = await get_user_by_email(db, form.username)
    if not user:
        raise BadRequestError("Incorrect email or password")

    if not verify_password(form.password, user.hashed_password):
        raise BadRequestError("Incorrect email or password")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)