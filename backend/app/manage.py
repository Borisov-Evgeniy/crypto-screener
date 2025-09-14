import typer
import subprocess
import asyncio
from backend.scripts import create_tables

app = typer.Typer(help="Управление проектом")

@app.command("init-db")
def init_db():
    """Создать таблицы в базе данных"""
    asyncio.run(create_tables.run())

@app.command("runserver")
def runserver(host: str = "0.0.0.0" , port: int=8000, reload: bool = True):
    """Запуск сервера FastAPI"""
    cmd = [
        "uvicorn",
        "backend.main:app"
        "--host",host,
        "--port",str(port),
    ]
    if reload:
        cmd.append("--reload")
    subprocess.run(cmd)

@app.command("alembic-upgrade")
def alembic_upgrade(revision: str="head"):
    """Применение миграции"""
    subprocess.run(["alembic","upgrade",revision])



if __name__ == "__main__":
    app()
