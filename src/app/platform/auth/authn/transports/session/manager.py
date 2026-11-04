import hashlib
import hmac
from typing import Any
from uuid import uuid4

from starlette.requests import Request
from user_agents import parse as _ua_parse

from app.platform.auth.authn.transports.session import constants
from app.platform.auth.authn.transports.session.schemas import SessionData, UserAgentInfo
from app.platform.config.settings import get_settings
from app.platform.storage.base import AbstractStore
from app.platform.util.http import get_client_ip

settings = get_settings()


class SessionManager:
    def __init__(
            self,
            *,
            store: AbstractStore,
            csrf: bool,
            key_secret: str | None = None,
            key_prefix: str,
            session_timeout_minutes: int,
            absolute_timeout_hours: int | None = None,


    ):
        self.store = store
        self.csrf = csrf
        self.key_secret = key_secret
        self.key_prefix = key_prefix
        self.session_timeout_minutes = session_timeout_minutes
        self.absolute_timeout_hours = absolute_timeout_hours

    # ====== storage keys =================================================
    def _keyed(self, purpose: bytes, value: str) -> str:
        if self.key_secret is None:
            return value
        return hmac.new(
            self.key_secret.encode(),
            purpose + value.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _session_key(self, session_id: str) -> str:
        return self._keyed(b'session:', session_id)

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid4())

    def _get_session_key(self, session_id: str) -> str:
        return f"{self.key_prefix}{session_id}"

    # ====== session lifecycle ============================================
    def _parse_user_agent(self, user_agent_string: str) -> UserAgentInfo:
        """Parse a UA string into structured device info."""
        ua = _ua_parse(user_agent_string)
        return UserAgentInfo(
            browser=ua.browser.family,
            browser_version=ua.browser.version_string,
            os=ua.os.family,
            device=ua.device.family,
            is_mobile=ua.is_mobile,
            is_tablet=ua.is_tablet,
            is_pc=ua.is_pc,
        )

    async def create_session(
            self,
            request: Request,
            user_id: str,
            metadata: dict[str, Any] | None = None,
            expiration: int | None = None,
            token_version: int | None = None,
    ):
        """Create a new session."""
        presented = request.headers.get(constants.SESSION_COOKIE_NAME, "")
        if presented:
            await self.terminate_session(presented)
        await self._enforce_session_limit(user_id)

        user_agent = request.headers.get("user-agent", "")
        device_info = self._parse_user_agent(user_agent)
        ip_addr = get_client_ip(request)

        session_data = SessionData(
            user_id=user_id,
            ip_addr=ip_addr,
            user_agent=user_agent,
            device_info=device_info,
            metadata=metadata or {},
            token_version=token_version,
        )

        session_id = self._generate_session_id()
        storage_session_key = self._get_session_key(session_id)

        await self.store.create(
            key=storage_session_key,
            data=session_data,
            expiration=expiration,
        )

    async def terminate_session(self, session_id: str):
        """Terminate an existing session."""

    # ====== session limit enforcement & cleanup =========================
    async def _enforce_session_limit(self, user_id: str):
        """Enforce the maximum number of sessions per user."""

    # ====== CSRF ========================================================
