import redis

def main():
    # Подключение к Redis через localhost (порт проброшен в docker-compose)
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # Проверка подключения
    try:
        if r.ping():
            print("✅ Redis подключён!")
    except redis.ConnectionError as e:
        print("❌ Не удалось подключиться к Redis:", e)
        return

    # Добавление тестового ключа
    r.set("test_key", "Hello Redis")
    print("Добавлен ключ 'test_key' со значением 'Hello Redis'")

    # Получение значения тестового ключа
    value = r.get("test_key")
    print(f"Значение test_key: {value}")

    # Вывод всех ключей и их значений
    print("\nВсе ключи в Redis:")
    keys = r.keys("*")
    if not keys:
        print("Ключи отсутствуют")
    else:
        for key in keys:
            val = r.get(key)
            print(f"{key}: {val}")

if __name__ == "__main__":
    main()
