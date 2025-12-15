from datetime import UTC, datetime

import redis.asyncio as aioredis
from fastapi import HTTPException, status

from app.config.config import Config, config


class RedisClient:
    """Асинхронный клиент Redis."""

    def __init__(self, config: Config):
        self.host = config.redis.host
        self.port = config.redis.port
        self.db = config.redis.db
        self.ttl = config.redis.ttl

        self.redis = aioredis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    async def add_event_zset(self, key: str) -> None:
        """Добавляет событие в ZSET с timestamp и очищает старые записи."""
        now_ts = int(datetime.now(UTC).timestamp())
        window_start = now_ts - 24 * 3600  # 24 часа назад

        try:
            # Удаляем старые значения
            await self.redis.zremrangebyscore(key, 0, window_start)

            # Добавляем новое событие
            await self.redis.zadd(key, {str(now_ts): now_ts})

            # Обновляем TTL
            await self.redis.expire(key, self.ttl)

        except aioredis.RedisError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f'Redis недоступен: {e}'
            ) from e

    async def get_events(self, key: str) -> list[int]:
        """Возвращает ВСЕ timestamp события из ZSET."""
        try:
            events = await self.redis.zrange(key, 0, -1)
            return [int(e) for e in events]
        except aioredis.RedisError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f'Redis недоступен: {e}'
            ) from e


def get_redis_client() -> RedisClient:
    """Клиент для DI."""
    return RedisClient(config=config)
