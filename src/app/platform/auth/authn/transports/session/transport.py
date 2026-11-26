import logging
from typing import Any, override

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from app.platform.auth.authn.constants import CSRF_HEADER_NAME, REMEMBER_ME_META_KEY, SAFE_METHODS, SESSION_COOKIE_NAME
from app.platform.auth.authn.core import AuthContext, Principal, SameSite, Transport, TransportName
from app.platform.auth.authn.exceptions import CSRFException
from app.platform.auth.authn.transports.session.manager import SessionManager
from app.platform.auth.authn.transports.session.routers import build_session_routes
from app.platform.auth.users.models import User
from app.platform.auth.users.service import UserService
from app.platform.constant.enums import AccountStatusEnum
from app.platform.storage.base import AbstractStore

logger = logging.getLogger(__name__)


class SessionTransport(Transport):
    def __init__(
            self,
            *,
            user_service: UserService,
            store: AbstractStore,
            csrf_enabled: bool,
            session_key_prefix: str,
            csrf_key_prefix: str | None = None,
            key_secret: str | None = None,
            session_timeout_minutes: int,
            absolute_timeout_enabled: bool | None = None,
            absolute_timeout_hours: int | None = None,
            remember_me_enabled: bool | None = None,
            remember_me_days: int | None = None,
            max_sessions_per_user: int | None = None,
            cookie_secure: bool = True,
            cookie_samesite: SameSite = "lax",
            cookie_path: str = "/",
    ):
        super().__init__(user_service=user_service)
        self.manager = SessionManager(
            store,
            csrf_enabled=csrf_enabled,
            session_key_prefix=session_key_prefix,
            csrf_key_prefix=csrf_key_prefix,
            key_secret=key_secret,
            session_timeout_minutes=session_timeout_minutes,
            absolute_timeout_enabled=absolute_timeout_enabled,
            absolute_timeout_hours=absolute_timeout_hours,
            remember_me_enabled=remember_me_enabled,
            remember_me_days=remember_me_days,
            max_sessions_per_user=max_sessions_per_user,
            cookie_secure=cookie_secure,
            cookie_samesite=cookie_samesite,
            cookie_path=cookie_path,
        )

    name: TransportName = "session"

    @override
    def contributes_routes(self) -> APIRouter | None:
        return build_session_routes(self)

    @override
    async def _authenticate_password(
            self,
            db: AsyncSession,
            identifier: str,
            password: str,
            *,
            request: Request,
    ) -> User:
        return await super()._authenticate_password(db, identifier, password, request=request)

    @override
    async def _complete_login(
            self,
            request: Request,
            response: Response,
            user: User,
            options: dict[str, Any],
    ) -> dict[str, Any]:
        remember_me = bool(options.get("remember_me"))
        metadata = dict(options.get("metadata") or {})
        if remember_me:
            metadata[REMEMBER_ME_META_KEY] = remember_me

        session_id, csrf_token = await self.manager.create_session(
            request,
            user.id,
            metadata=metadata,
            token_version=user.token_version,
        )

        cookie_max_age = self.manager.timeout_seconds_for(metadata) if remember_me else None

        self.manager.set_session_cookies(response, session_id, csrf_token, cookie_max_age)

        return {
            "id": user.id,
            "username": user.name,
            "csrf_token": csrf_token,
        }

    async def authenticate(self, auth_context: AuthContext) -> Principal | None:
        session_id = auth_context.request.cookies.get(SESSION_COOKIE_NAME)
        if not session_id:
            logger.warning("No session id found in cookies")
            return None

        session_data = await self.manager.validate_session(session_id, auth_context.enforce_csrf)
        if session_data is None:
            logger.warning("Invalid session")
        if session_data is None:
            return None

        if auth_context.enforce_csrf:
            await self.enforce_csrf(auth_context.request, session_id)

        user = await auth_context.resolve_user(session_data.user_id, self.user_service)

        if (user is None
                or user.account_status != AccountStatusEnum.ACTIVE):
            logger.warning("User is inactive or does not exist")
            return None

        return auth_context.build_principal(user_id=user.id, user=user)

    async def enforce_csrf(self, request: Request, session_id: str) -> None:
        """Require a valid synchronizer-token header on unsafe methods.

        Note:
            Header-only by design: the ``csrf_token`` cookie auto-rides
            cross-origin requests but a custom header does not, so requiring the
            header (not just the cookie) is what makes the synchronizer-token check
            load-bearing. Safe methods (GET/HEAD/OPTIONS) are exempt.
        """
        if request.method in SAFE_METHODS:
            return
        header = request.headers.get(CSRF_HEADER_NAME)
        if not header:
            raise CSRFException("Missing CSRF token")
        if not await self.manager.validate_csrf_token(session_id, header):
            raise CSRFException("Invalid CSRF token")
