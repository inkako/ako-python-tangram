from app.platform.auth.authn.core import Principal, Transport
from app.platform.auth.authn.exceptions import UnauthenticatedException
from app.platform.auth.authn.resolution import PrincipalResolver
from app.platform.dependency import AsyncSessionDep
from app.platform.logging import get_logger
from app.platform.storage.base import AbstractStore
from fastapi import Request

logger = get_logger(__name__)


class CoAuthn:
    def __int__(
            self,
            transport: Transport,
            *,
            store: AbstractStore,
    ):
        self.transport = transport
        self.store = store
        self._resolver = PrincipalResolver(self.transport)

    async def current_user(
            self,
            request: Request,
            db_session: AsyncSessionDep
    ) -> Principal:
        """Get the current user."""
        principal = await self._resolver.resolve(request, db_session)
        if principal is None:
            raise UnauthenticatedException("Not authenticated")
        return principal


co_authn = CoAuthn(

)


def get_co_authn() -> CoAuthn:
    return co_authn
