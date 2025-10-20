from redis.asyncio import Redis
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_redis():
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.aclose()

async def add(key: str, value: str, ttl: int = None) -> bool:
    async with get_redis() as redis:
        return await redis.set(key, value, ex=ttl)

async def get(key: str) -> str | None:
    async with get_redis() as redis:
        return await redis.get(key)