from typing import TYPE_CHECKING, Any, Annotated

from fastapi import APIRouter, Request, Response, Form

from app.platform.auth.authn.dependencies import OAuth2FormDep
from app.platform.auth.authn.exceptions import ForbiddenException
from app.platform.dependency import AsyncSessionDep
from app.platform.logging import get_logger
from app.platform.util import is_cross_site

if TYPE_CHECKING:
    from app.platform.auth.authn.transports.session.transport import SessionTransport

logger = get_logger(__name__)


def build_session_routes(transport: "SessionTransport") -> APIRouter:
    router = APIRouter(tags=["authentication"])

    @router.post("/login")
    async def login(
            request: Request,
            response: Response,
            form_data: OAuth2FormDep,
            db: AsyncSessionDep,
            remember_me: Annotated[bool, Form()] = False,
    ) -> dict[str, Any]:
        """Login endpoint to get session cookies."""

        if is_cross_site(request):
            raise ForbiddenException("Cross-site login are not allowed.")

        return await transport.password_login(
            db=db,
            request=request,
            response=response,
            form_data=form_data,
        )

    return router
