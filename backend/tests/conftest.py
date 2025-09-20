import os
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from backend.app.models.user import Base
from backend.app.repositories.user_repositories import UserRepository
from backend.app.services.user_service import UserService

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
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.session = self.async_session()
        return self

    async def teardown(self):
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
        return UserRepository(self.get_session())

# --- фикстуры --- #

@pytest_asyncio.fixture
async def db():
    d = DatabaseFixture(DATABASE_URL)
    await d.setup_table()
    try:
        yield d
    finally:
        await d.teardown()

@pytest_asyncio.fixture
async def user_repository(db):
    yield db.get_user_repo()

@pytest_asyncio.fixture
async def user_service(db):
    repo = db.get_user_repo()
    service = UserService(repo)
    yield service
