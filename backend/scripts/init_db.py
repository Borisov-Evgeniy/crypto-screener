import asyncio
from backend.app.db.session import engine, Base

async def run():
    """Создание таблиц в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(run())