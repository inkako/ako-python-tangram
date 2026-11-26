from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Form, Request, Response

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

    @router.post("/logout")
    async def logout(
            request: Request,
            response: Response,
            db: AsyncSessionDep,
    ) -> dict[str, Any]:
        """Revoke the current session and clear the auth cookies (CSRF-protected).

        Clears every configured transport's cookies, including a bearer refresh
        cookie. A session that already expired has nothing left to protect, so
        its cookies are cleared without a CSRF check. The body of
        [complete_logout][crudauth.transports.session.transport.SessionTransport.complete_logout].
        """

        if is_cross_site(request):
            raise ForbiddenException("Cross-site logout are not allowed.")

        await transport.complete_logout(
            db=db,
            request=request,
            response=response,
        )

        return {"detail": "Logged out"}

    return router
