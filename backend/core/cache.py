import redis.asyncio as aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_cached_verdict(x, y):
    return await redis.get(f"verdict:{x.lower()}:{y.lower()}")

async def cache_verdict(x, y, verdict):
    await redis.set(f"verdict:{x.lower()}:{y.lower()}", verdict, ex=86400)