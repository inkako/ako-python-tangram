from app.platform.auth.authn.core import Transport, Principal
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


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
            transport: Transport
    ) -> Principal:
        ...
