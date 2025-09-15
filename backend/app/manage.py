import typer
import subprocess
import asyncio
from backend.scripts import create_tables

app = typer.Typer(help="Управление проектом")

@app.command("init-db")
def init_db():
    """Создать таблицы в базе данных"""
    run_fn = getattr(create_tables, "run", None)
    if run_fn is None:
        print("create_tables.run не найден")
        return
    # Если run_fn асинхронная — запустим через asyncio, иначе вызовем напрямую
    if asyncio.iscoroutinefunction(run_fn):
        asyncio.run(run_fn())
    else:
        run_fn()

@app.command("runserver")
def runserver(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Запуск сервера FastAPI"""
    cmd = [
        "uvicorn",
        "backend.app.main:app",
        "--host", host,
        "--port", str(port),
    ]
    if reload:
        cmd.append("--reload")
    # check=True чтобы получить non-zero exit из subprocess в случае ошибок
    subprocess.run(cmd, check=True)

@app.command("alembic-upgrade")
def alembic_upgrade(revision: str = "head"):
    """Применение миграции"""
    subprocess.run(["alembic", "upgrade", revision], check=True)

if __name__ == "__main__":
    app()
