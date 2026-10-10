from abc import abstractmethod, ABC
from typing import Any

from app.platform.auth.constants import DEFAULT_SESSION_TTL_SECONDS
from pydantic import BaseModel


class AbstractSessionStorage[SessionModel: BaseModel](ABC):
    @abstractmethod
    async def create(
            self,
            data: SessionModel,
            session_id: str | None = None,
            expiration: int = DEFAULT_SESSION_TTL_SECONDS,
    ) -> Any:
        ...
