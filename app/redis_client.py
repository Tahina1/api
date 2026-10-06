from redis.asyncio import Redis

from app.config import settings

def create_redis() -> Redis:
    # decode_responses=True : Redis return str instead of bytes
    return Redis.from_url(settings.redis_url, decode_responses=True)