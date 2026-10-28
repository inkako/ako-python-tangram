from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from app.platform.auth.authn.constants import DEFAULT_SESSION_TTL_SECONDS


class AbstractStore[ValueModel: BaseModel](ABC):
    @abstractmethod
    async def create(
        self,
        data: ValueModel,
        session_id: str | None = None,
        expiration: int = DEFAULT_SESSION_TTL_SECONDS,
    ) -> Any:
        ...
