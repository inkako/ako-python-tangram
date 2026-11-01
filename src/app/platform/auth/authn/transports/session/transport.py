from typing import Any, override

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from app.platform.auth.authn.transport import Transport
from app.platform.auth.authn.transports.session.routers import build_session_routers
from app.platform.auth.users.models import User


class SessionTransport(Transport):
    def __init__(
            self,
            *,
            store: Any,
            csrf: bool = True,

    ):
        self.store = store
        self.csrf = csrf

    @override
    def contributes_routes(self) -> APIRouter | None:
        return build_session_routers(self)

    @override
    async def complete_login(
            self,
            request: Request,
            response: Response,
            user: User,
    ) -> dict[str, Any]:
        pass

