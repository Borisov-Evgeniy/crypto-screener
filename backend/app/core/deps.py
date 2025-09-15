from typing import AsyncGenerator
from backend.app.db import async_session_maker

async def get_db() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session