from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.app.schemas.user import UserCreate, UserRead, UserLogin, EmailUpdate, PasswordUpdate, StatusUpdate
from backend.app.db.session import get_db
from backend.app.repositories.user_repositories import UserRepository, UserNotFoundError,InvalidPasswordError
from backend.app.services.user_service import UserService

router = APIRouter()

def get_user_service(session: AsyncSession = Depends(get_db())) -> UserService: # для http запросов
    repo = UserRepository(session)
    return UserService(repo)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    """Регистрация пользователя. Принимает email и password
    возвращает созданного пользователя без пароля"""
    try:
        user = await service.create_user(payload.email, payload.password)
    except ValueError as e:
        # если пользователь существует
        raise HTTPException(status_code=400,detail=str(e))
    return user

@router.post("/auth", response_model=UserRead)
async def auth(payload: UserLogin, service: UserService = Depends(get_user_service)):
    """Упрощённая авторизация. Проверяем почту и пароль и возвращаем объкет user
    позже замена возврат JWT token"""
    user = await service.authenticate_user(payload.email,payload.password)
    if not user:
        raise HTTPException(status_code=401,detail='Invalid credentials')
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_user_service))
    """Ищем пользователя по id и возвращаем user"""
    try:
        user = await service.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"{user_id} not found")
    except UserNotFoundError as e:
        raise HTTPException(status_code=401,detail=str(e))
    return user


