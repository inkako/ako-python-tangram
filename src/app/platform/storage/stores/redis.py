from typing import Any, override

from pydantic import BaseModel
from redis.asyncio import Redis

from app.platform.config.settings import get_settings
from app.platform.storage.base import AbstractStore


class RedisStore[ValueModel: BaseModel](AbstractStore[ValueModel]):
    def __init__(self, url: str):
        self.client = Redis.from_url(url, decode_responses=False)

    @override
    async def create(
            self,
            key: str,
            data: ValueModel,
            expiration: int,
    ) -> Any:
        payload = data.model_dump_json().encode()
        await self.client.set(key, payload, ex=expiration)

    @override
    async def retrieve(
            self,
            key: str,
            model_class: type[ValueModel],
    ) -> ValueModel | None:
        raw = await self.client.get(key)
        if raw is None:
            return None
        return model_class.model_validate_json(raw)


settings = get_settings()
redis_store = RedisStore(settings.REDIS_URL)


def get_redis_store():
    return redis_store
