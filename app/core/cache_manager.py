from typing import Optional, Any
from redis import Redis
from contextlib import contextmanager
from flask import Config


class CacheManager:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    @contextmanager
    def get_connection(self):
        redis = Redis(
            host=self.config['REDIS_HOST'],
            port=self.config['REDIS_PORT'],
            db=0
        )
        try:
            yield redis
        finally:
            redis.close()

    def get(self, key: str) -> Optional[bytes]:
        # Get the value from the cache based on the key
        with self.get_connection() as redis:
            return redis.get(key)

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        # Set the value in the cache based on the key with an optional expiration time
        with self.get_connection() as redis:
            if expire:
                redis.setex(key, expire, value)
            else:
                redis.set(key, value)
