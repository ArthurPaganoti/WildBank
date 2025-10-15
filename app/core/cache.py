import redis.asyncio as redis
from typing import Optional, Any
import pickle
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

class RedisCache:
    _instance: Optional[redis.Redis] = None

    @classmethod
    async def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            try:
                redis_url = getattr(settings, 'redis_url', None)
                redis_host = getattr(settings, 'redis_host', 'localhost')

                if redis_url:
                    cls._instance = redis.from_url(
                        redis_url,
                        encoding="utf-8",
                        decode_responses=False
                    )
                else:
                    redis_port = getattr(settings, 'redis_port', 6379)
                    redis_db = getattr(settings, 'redis_db', 0)
                    redis_password = getattr(settings, 'redis_password', None)

                    cls._instance = redis.Redis(
                        host=redis_host,
                        port=redis_port,
                        db=redis_db,
                        password=redis_password if redis_password else None,
                        decode_responses=False
                    )

                await cls._instance.ping()
                logger.info("redis_connected", host=redis_host if not redis_url else "url")
            except Exception as e:
                logger.warning("redis_connection_failed", error=str(e))
                cls._instance = None

        return cls._instance

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        try:
            client = await cls.get_instance()
            if client is None:
                return None

            value = await client.get(key)
            if value:
                logger.debug("cache_hit", key=key)
                return pickle.loads(value)

            logger.debug("cache_miss", key=key)
            return None
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None

    @classmethod
    async def set(cls, key: str, value: Any, expire: int = 300) -> bool:
        try:
            client = await cls.get_instance()
            if client is None:
                return False

            serialized = pickle.dumps(value)
            await client.set(key, serialized, ex=expire)
            logger.debug("cache_set", key=key, expire=expire)
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False

    @classmethod
    async def delete(cls, key: str) -> bool:
        try:
            client = await cls.get_instance()
            if client is None:
                return False

            await client.delete(key)
            logger.debug("cache_deleted", key=key)
            return True
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False

    @classmethod
    async def clear_pattern(cls, pattern: str) -> int:
        try:
            client = await cls.get_instance()
            if client is None:
                return 0

            keys = []
            async for key in client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted = await client.delete(*keys)
                logger.info("cache_pattern_cleared", pattern=pattern, count=deleted)
                return deleted

            return 0
        except Exception as e:
            logger.error("cache_clear_pattern_error", pattern=pattern, error=str(e))
            return 0

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.aclose()
            cls._instance = None
            logger.info("redis_connection_closed")


async def get_cache(key: str) -> Optional[Any]:
    return await RedisCache.get(key)


async def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    return await RedisCache.set(key, value, expire)


async def delete_cache(key: str) -> bool:
    return await RedisCache.delete(key)
