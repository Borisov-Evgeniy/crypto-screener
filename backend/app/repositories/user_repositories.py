from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> User:
        user = User(email=email, hashed_password=password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def update_user_email(self, user_id: int, new_email: str) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.email = new_email
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def change_user_status(self, user_id: int, is_active: bool) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.is_active = is_active
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
