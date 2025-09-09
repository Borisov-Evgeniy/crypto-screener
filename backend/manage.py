import typer
from backend.scripts import create_tables

app = typer.Typer(help="Управление проектом")

@app.command("init-db")
def init_db():
    """Создать таблицы в базе данных"""
    create_tables.run()

if __name__ == "__main__":
    app()
