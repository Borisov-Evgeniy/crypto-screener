import psycopg2
import redis
from backend.app.core.config import settings

#Проверка PostgreSQL
try:
    conn = psycopg2.connect(settings.POSTGRES_DSN)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    print(f"PostgreSQL connection OK, test query returned: {result[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"PostgreSQL connection FAILED: {e}")

# Проверка Redis
try:
    r = redis.Redis.from_url(settings.REDIS_DSN)
    pong = r.ping()
    print(f"Redis connection OK, PING returned: {pong}")
except Exception as e:
    print(f"Redis connection FAILED: {e}")
