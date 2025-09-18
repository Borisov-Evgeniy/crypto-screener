from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.user import User
from backend.app.core.security import password_hasher


class UserNotFoundError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> User:
        """Создаёт экземпляр User, хеширует пароль и сохраняет в БД."""
        hashed_password = password_hasher.hasher(password)
        user = User(email=email, hashed_password=hashed_password)

        # добавляем экземпляр (не класс* для себя))
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Возвращает User или None."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first() # возвращает объект модели или None

    async def verify_password_user(self, email: str, password: str) -> bool:
        """Проверяет пароль, кидает исключения в случае ошибки."""
        user = await self.get_user_by_email(email)
        if user is None:
            raise UserNotFoundError(f"User with email {email} not found")

        hashed = getattr(user, "hashed_password", None)
        if hashed is None:
            raise InvalidPasswordError("User has no password set")

        if not password_hasher.verify_password(password, hashed):
            raise InvalidPasswordError("Incorrect password")
        return True

    async def delete_user(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(f"User id: {user_id} not found")
        self.session.delete(user)
        await self.session.commit()

    async def update_user_email(self, user_id: int, new_email: str) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(f"User id: {user_id} not found")
        user.email = new_email
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def user_password(self, user_id: int, new_password: str) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(f"User id: {user_id} not found")
        user.hashed_password = password_hasher.hasher(new_password)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def change_user_status(self, user_id: int, is_active: bool) -> str:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(f"User id: {user_id} not found")
        user.is_active = is_active
        await self.session.commit()
        await self.session.refresh(user)

        action = "activated" if is_active else "deactivated"
        return f'Пользователь {user_id} - {action}'