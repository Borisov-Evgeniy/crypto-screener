from backend.app.db.session import engine
from backend.app.models import user

def run():
    print("Создаю таблицы...")
    user.Base.metadata.create_all(bind=engine)
    print("Готово!")

if __name__ == "__main__":
    run()