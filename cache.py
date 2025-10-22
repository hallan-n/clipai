import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def add(key: str, value: str, ttl: int = None) -> bool:
    return redis_client.set(name=key, value=value, ex=ttl)

def get(key: str) -> str | None:
    return redis_client.get(key)
