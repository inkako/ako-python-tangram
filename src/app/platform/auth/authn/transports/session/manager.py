import hashlib
import hmac
import secrets
from datetime import timedelta
from typing import Any
from uuid import uuid4

from starlette.requests import Request
from user_agents import parse as _ua_parse

from app.platform.auth.authn.constants import (
    CSRF_TOKEN_BYTES,
    REMEMBER_ME_META_KEY,
    USER_INDEX_SUFFIX,
    USER_INDEX_TTL_BUFFER_SECONDS,
    SESSION_COOKIE_NAME,
    CSRF_TOKEN_ID_META_KEY,
)
from app.platform.auth.authn.transports.session.schemas import CSRFToken, SessionData, UserAgentInfo
from app.platform.config.settings import get_settings
from app.platform.logging import get_logger
from app.platform.storage.base import AbstractStore
from app.platform.util import utcnow
from app.platform.util.http_utils import get_client_ip

logger = get_logger(__name__)

settings = get_settings()


class SessionManager:
    def __init__(
            self,
            store: AbstractStore,
            *,
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
            cookie_samesite: str = "lax",
            cookie_path: str = "/",
    ):
        self.store = store
        self.csrf_enabled = csrf_enabled
        self.session_key_prefix = session_key_prefix
        self.csrf_key_prefix = csrf_key_prefix
        self.key_secret = key_secret
        self.session_timeout_minutes = timedelta(minutes=session_timeout_minutes)
        self.absolute_timeout_enabled = absolute_timeout_enabled
        self.absolute_timeout_hours = timedelta(hours=absolute_timeout_hours)
        self.remember_me_enabled = remember_me_enabled
        self.remember_me_days = timedelta(days=remember_me_days)
        self.max_sessions_per_user = max_sessions_per_user
        self.cookie_secure = cookie_secure
        self.cookie_samesite = cookie_samesite
        self.cookie_path = cookie_path

    # ======================================================================
    # storage keys
    # ======================================================================
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

    def _csrf_key(self, token: str) -> str:
        return self._keyed(b'csrf:', token)

    def _handle_of(self, key: str) -> str:
        if self.key_secret is None:
            return hashlib.sha256(key.encode()).hexdigest()
        return key

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid4())

    @staticmethod
    def _generate_csrf_token() -> str:
        return secrets.token_hex(CSRF_TOKEN_BYTES)

    def _get_session_storage_key(self, key: str, *, is_raw: bool = True) -> str:
        if is_raw:
            return f"{self.session_key_prefix}{key}"
        return f"{self.session_key_prefix}{self._session_key(key)}"

    def _get_csrf_storage_key(self, key: str, *, is_raw: bool = True) -> str:
        if is_raw:
            return f"{self.csrf_key_prefix}{key}"
        return f"{self.csrf_key_prefix}{self._csrf_key(key)}"

    def _user_index_storage_key(self, user_id: str) -> str:
        user_index_prefix = f"{self.session_key_prefix}{USER_INDEX_SUFFIX}"
        return f"{user_index_prefix}{user_id}"

    # ======================================================================
    # timeout helpers
    # ======================================================================
    def timeout_for_seconds(self, metadata: dict[str, Any] | None = None) -> int:
        """Determine the session timeout in seconds."""
        if metadata and metadata.get(REMEMBER_ME_META_KEY):
            return int(self.remember_me_days.total_seconds())
        return int(self.session_timeout_minutes.total_seconds())

    # ======================================================================
    # session lifecycle
    # ======================================================================
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

    async def _index_user_sessions(
            self,
            user_id: str,
            session_id_raw: str,
            expiration: int,
    ):
        """Index user sessions."""
        user_index_key = self._user_index_storage_key(user_id)
        ttl = expiration + USER_INDEX_TTL_BUFFER_SECONDS
        await self.store.sadd(
            key=user_index_key,
            member=session_id_raw,
            expiration=ttl,
        )

    async def create_session(
            self,
            request: Request,
            user_id: str,
            metadata: dict[str, Any] | None = None,
            expiration_seconds: int | None = None,
            token_version: int | None = None,
    ) -> tuple[str, str]:
        """Create a new session."""
        presented = request.headers.get(SESSION_COOKIE_NAME, "")
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
        session_id_raw = self._session_key(session_id)
        session_storage_key = self._get_session_storage_key(session_id_raw)

        ttl = (
            expiration_seconds
            if expiration_seconds is not None
            else self.timeout_for_seconds(session_data.metadata)
        )

        session_data.session_id_raw = session_id_raw

        csrf_token: str = ""
        if self.csrf_enabled:
            csrf_token, csrf_token_raw = self._create_csrf_token(session_id_raw, ttl)
            session_data.metadata[CSRF_TOKEN_ID_META_KEY] = csrf_token_raw

        await self._index_user_sessions(
            user_id=user_id,
            session_id_raw=session_id_raw,
            expiration=ttl,
        )

        await self.store.set(
            key=session_storage_key,
            data=session_data,
            expiration=ttl,
        )

        return session_id, csrf_token

    async def terminate_session(
            self,
            session_id: str,
            reason: str | None = None
    ) -> bool:
        """Terminate an existing session."""
        session_storage_key = self._get_session_storage_key(session_id, is_raw=False)
        session_data = await self.store.get(session_storage_key, SessionData)
        if session_data is None:
            return False
        return await self._terminate(session_storage_key, session_data, reason)

    async def _terminate(
            self,
            session_storage_key: str,
            session_data: SessionData,
            reason: str | None = None
    ) -> bool:
        logger.warning("Terminating session %s for user %s (reason=%s)",
                       self._handle_of(session_storage_key), session_data.user_id, reason=reason)
        # delete session
        delete = await self.store.delete(session_storage_key)
        if delete:
            # delete index
            await self.store.srem(
                key=self._user_index_storage_key(session_data.user_id),
                member=session_data.session_id_raw,
            )
        # delete csrf
        ...

    # ======================================================================
    # session limit enforcement & cleanup
    # ======================================================================
    async def _enforce_session_limit(self, user_id: str):
        """Enforce the maximum number of sessions per user."""

    # ======================================================================
    # CSRF
    # ======================================================================
    async def _create_csrf_token(
            self,
            session_id: str,
            ttl: int,
    ) -> tuple[str, str]:
        """Generate a CSRF token."""
        token = self._generate_csrf_token()
        token_raw = self._csrf_key(token)
        token_data = CSRFToken(
            token=token_raw,
            session_id=session_id,
            expiry=utcnow() + timedelta(seconds=ttl),
        )
        token_storage_key = self._get_csrf_storage_key(token_raw)
        await self.store.set(
            key=token_storage_key,
            data=token_data,
            expiration=ttl,
        )
        return token, token_raw

    # ======================================================================
    # cookies
    # ======================================================================
