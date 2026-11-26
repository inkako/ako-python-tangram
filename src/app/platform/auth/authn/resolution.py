from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.platform.auth.authn.core import AuthContext, Principal, Transport


class PrincipalResolver:
    def __init__(
            self,
            transport: Transport,
    ):
        self.transport = transport

    async def resolve(
            self,
            request: Request,
            db_session: AsyncSession,
            *,
            enforce_csrf: bool = True,
    ) -> Principal:
        """Resolve the principal for the given request and transport."""
        # cache todo

        # construct an authentication context
        ctx = self._auth_ctx(request, db_session, enforce_csrf)

        # get principal by authenticate with transport
        return await self.transport.authenticate(ctx)

    @classmethod
    def _auth_ctx(
            cls,
            request: Request,
            db_session: AsyncSession,
            enforce_csrf: bool,
    ) -> AuthContext:
        return AuthContext(
            request=request,
            db_session=db_session,
            enforce_csrf=enforce_csrf,
        )
