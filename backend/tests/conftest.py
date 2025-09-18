import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend.app.models.user import Base
from backend.repositories.user_repositories import UserRepository

load_dotenv()

DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set in .env")

class DatabaseFixture:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, future=True, echo=False)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.session: AsyncSession | None = None

    async def setup_table(self):
        # Создаём таблицы (если нужно — можно сначала дропнуть)
        async with self.engine.begin() as conn:
            # безопасно: создаст таблицы, если их нет
            await conn.run_sync(Base.metadata.create_all)
        # создаём сессию (экземпляр AsyncSession)
        self.session = self.async_session()
        return self

    async def teardown(self):
        # корректно закрываем сессию и роняем таблицы
        if self.session:
            await self.session.close()
            self.session = None
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await self.engine.dispose()

    def get_session(self) -> AsyncSession:
        if not self.session:
            raise RuntimeError("Сессия не открыта, сначала вызови setup_table()")
        return self.session

    def get_user_repo(self) -> UserRepository:
        return UserRepository(self.get_session()) # Возвращаем репозиторий, используя текущую сессию


@pytest.fixture
async def db():
    """
    Сессия и временная схема для тестов.
    Для доступа к сессии db.get_session().
    """
    d = DatabaseFixture(DATABASE_URL)
    await d.setup_table()
    try:
        yield d
    finally:
        await d.teardown()


@pytest.fixture
async def user_repo(db):
    """
    Фикстура, возвращающая  UserRepository, привязанный к тестовой базе.
    """
    yield db.get_user_repo()