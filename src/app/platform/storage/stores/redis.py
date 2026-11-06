from typing import Any, override

from pydantic import BaseModel
from redis.asyncio import Redis

from app.platform.config.settings import get_settings
from app.platform.storage.base import AbstractStore


class RedisStore[T: BaseModel](AbstractStore[T]):
    def __init__(self, url: str):
        self.client = Redis.from_url(url, decode_responses=False)

    @override
    async def set(
            self,
            key: str,
            data: Any,
            expiration: int,
    ) -> Any:
        payload = data
        if isinstance(data, BaseModel):
            payload = data.model_dump_json().encode("utf-8")
        await self.client.set(key, payload, ex=expiration)

    @override
    async def get(
            self,
            key: str,
            model_class: type[T] | None = None,
    ) -> BaseModel | str | None:
        raw = await self.client.get(key)
        if raw is None:
            return None
        if model_class is not None and issubclass(model_class, BaseModel):
            return model_class.model_validate_json(raw)
        return raw.decode("utf-8")

    @override
    async def delete(
            self,
            key: str,
    ) -> int:
        return await self.client.delete(key)

    @override
    async def sadd(
            self,
            key: str,
            member: Any,
            expiration: int,
    ):
        if isinstance(member, BaseModel):
            member = member.model_dump_json().encode("utf-8")
        async with self.client.pipeline(transaction=True) as pipe:
            pipe.sadd(key, member)
            pipe.expire(key, expiration, nx=True)
            pipe.expire(key, expiration, gt=True)
            await pipe.execute()

    async def smembers(self, key: str, model_class: type[T] | None = None) -> list[Any]:
        members = await self.client.smembers(key)
        if model_class is not None and issubclass(model_class, BaseModel):
            return [model_class.model_validate_json(m) for m in members]
        return [m.decode("utf-8") for m in members]

    @override
    async def srem(
            self,
            key: str,
            member: Any,
    ) -> int:
        if isinstance(member, BaseModel):
            member = member.model_dump_json().encode("utf-8")
        return await self.client.srem(key, member)


settings = get_settings()
redis_store = RedisStore(settings.REDIS_URL)


def get_redis_store():
    return redis_store
