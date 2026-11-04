from typing import Any, override

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from app.platform.auth.authn.constants import TRANSPORT
from app.platform.auth.authn.principal import Principal
from app.platform.auth.authn.transport import Transport
from app.platform.auth.authn.transports import session
from app.platform.auth.authn.transports.session.manager import SessionManager
from app.platform.auth.authn.transports.session.routers import build_session_routes
from app.platform.auth.users.models import User
from app.platform.auth.users.service import UserService
from app.platform.storage.base import AbstractStore


class SessionTransport(Transport):
    def __init__(
            self,
            *,
            store: AbstractStore,
            csrf: bool = True,
            user_service: UserService,

    ):
        super().__init__(user_service=user_service)
        self.store = store
        self.csrf = csrf
        self.manager = SessionManager(store=store)

    name: TRANSPORT = session

    @override
    def contributes_routes(self) -> APIRouter | None:
        return build_session_routes(self)

    @override
    async def _complete_login(
            self,
            request: Request,
            response: Response,
            user: User,
    ) -> dict[str, Any]:
        ...

    async def authenticate(self, request: Request) -> Principal | None:
        pass
