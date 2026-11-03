from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AbstractStore[ValueModel: BaseModel](ABC):

    @abstractmethod
    async def create(
            self,
            key: str,
            data: ValueModel,
            expiration: int,
    ) -> Any:
        ...

    @abstractmethod
    async def retrieve(
            self,
            key: str,
            model_class: type[ValueModel],
    ) -> ValueModel | None:
        ...
