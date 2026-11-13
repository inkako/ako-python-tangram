from fastapi import Request

from app.platform.auth.authn.core import Principal, Transport
from app.platform.logging import get_logger
from app.platform.storage.base import AbstractStore

logger = get_logger(__name__)


class CoAuthn:
    def __int__(
            self,
            transport: Transport,
            *,
            store: AbstractStore,
    ):
        self.transports = transport
        self.store = store

    def current_user(
            self,
            request: Request,
    ) -> Principal:
        """Get the current user."""



co_authn = CoAuthn(

)


def get_co_authn() -> CoAuthn:
    return co_authn
