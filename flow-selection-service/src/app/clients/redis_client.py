import json
from typing import Any

import redis

from app.config.config import Config, config


class RedisClient:
    """Клиент Redis."""

    def __init__(self, config: Config):
        self.host=config.redis.host
        self.port=config.redis.port
        self.db=config.redis.db
        self.decode_responses=True
        self.ttl=config.redis.ttl

        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    def get_from_cache(self, key: str) -> Any | None:
        """Получение объекта из Redis по ключу."""
        value = self.redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set_to_cache(self, key: str, value: Any):
        """Сохранение объекта в Redis с TTL."""
        json_value = json.dumps(value)
        self.redis_client.setex(key, self.ttl, json_value)


def get_redis_client() -> RedisClient:
    """Клиент для DI."""
    return RedisClient(config=config)
