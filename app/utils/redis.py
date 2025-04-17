import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter

from app.core.config import settings


async def init_redis() -> redis.Redis:
    """Initialize Redis connections for rate limiting and caching.

    Returns:
        The initialized redis connection object.
    Raises:
        Exception: If the connection fails.
    """
    redis_url = f"redis://{settings.REDISUSER}:{settings.REDISPASSWORD}@{settings.REDISHOST}:{settings.REDISPORT}"
    try:
        red = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(red)
        FastAPICache.init(RedisBackend(red), prefix="fastapi-cache")
        return red
    except Exception as e:
        raise Exception(f"Redis connection failed: {str(e)}")


async def check_redis_health() -> str:
    """Check Redis connection health."""
    redis_url = f"redis://{settings.REDISUSER}:{settings.REDISPASSWORD}@{settings.REDISHOST}:{settings.REDISPORT}"
    try:
        red = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await red.ping()
        return "healthy"
    except Exception:
        return "unhealthy"
