from backend.app.db.session import engine
from sqlalchemy import inspect
import asyncio

async def check_tables():
    async with engine.begin() as conn:
        def do_inspect(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables = await conn.run_sync(do_inspect)
        print("Таблицы в БД:", tables)

if __name__ == "__main__":
    asyncio.run(check_tables())
