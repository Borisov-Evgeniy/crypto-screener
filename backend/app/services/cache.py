from backend.app.core.redis_client import redis_client
import json

def cache_set(key: str,value: dict, expire_seconds: int=30):
    redis_client.setex(key,expire_seconds,json.dumps(value))

def cache_get(key: str):
    res = redis_client.get(key)
    return json.loads(res) if res else None