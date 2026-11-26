from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel


class AbstractStore[T: BaseModel](ABC):

    @abstractmethod
    async def set(
            self,
            key: str,
            data: Any,
            expiration: int,
    ) -> Any:
        ...

    @abstractmethod
    async def get(
            self,
            key: str,
            model_class: type[T] | None = None,
    ) -> T | None:
        ...

    @abstractmethod
    async def delete(
            self,
            key: str,
    ) -> bool:
        ...

    @abstractmethod
    async def sadd(
            self,
            key: str,
            member: Any,
            expiration: int,
    ):
        ...

    @abstractmethod
    async def smembers(
            self,
            key: str,
    ) -> list[Any]:
        ...

    @abstractmethod
    async def srem(
            self,
            key: str,
            member: Any,
    ) -> int:
        ...

    @abstractmethod
    async def modify(
            self,
            key: str,
            model_class: type[T],
            change: Callable[[T], None],
            reset_expiration: bool = True,
            expiration: int | None = None,
    ) -> T | None:
        ...

    @abstractmethod
    async def extend(self, key: str, expiration: int) -> bool:
        ...
