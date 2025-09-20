from backend.app.core.security import password_hasher
from backend.app.models.user import User
from backend.app.repositories.user_repositories import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, password: str) -> User:
        hashed_password = password_hasher.hasher(password)
        return await self.user_repository.create_user(email=email, password=hashed_password)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not password_hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def change_password(self, user_id: int, new_password: str) -> User | None:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        user.hashed_password = password_hasher.hasher(new_password)
        await self.user_repository.session.commit()
        await self.user_repository.session.refresh(user)
        return user

    async def change_email(self, user_id: int, new_email: str) -> User | None:
        return await self.user_repository.update_user_email(user_id, new_email)

    async def change_status(self, user_id: int, is_active: bool) -> User | None:
        return await self.user_repository.change_user_status(user_id, is_active)

    async def delete_user(self, user_id: int) -> None:
        return await self.user_repository.delete_user(user_id)
