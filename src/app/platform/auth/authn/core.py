from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from app.platform.auth.authn.exceptions import UnauthenticatedException
from app.platform.auth.users.models import User
from app.platform.auth.users.service import UserService
from app.platform.constant.enums import AccountStatusEnum
from app.platform.logging import get_logger
from app.platform.util import canonical_identifier, verify_password

logger = get_logger(__name__)

# Transport
TransportName = Literal["session", "bearer"]

# SameSite
SameSite = Literal["lax", "strict", "none"]


@dataclass
class CookieConfig:
    secure: bool
    samesite: SameSite
    path: str


@dataclass(frozen=True)
class Principal:
    user_id: Any
    user: User = None
    is_superuser: bool = False


class Transport(ABC):
    def __init__(
            self,
            user_service: UserService,
    ):
        self.user_service = user_service

    name: TransportName | None = None

    def contributes_routes(self) -> APIRouter | None:
        return None

    async def _authenticate_password(
            self,
            db: AsyncSession,
            identifier: str,
            password: str,
            *,
            request: Request,
    ) -> User:
        login_id = canonical_identifier(identifier)

        user = await self.user_service.get(db, username=login_id)
        if user is None:
            logger.warning("Invalid username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        if AccountStatusEnum.ACTIVE != user.account_status:
            logger.warning("User is not active, username: %s, account_status: %s", login_id, user.account_status)
            raise UnauthenticatedException("User is not active")

        is_passed = verify_password(password, user.password)
        if not is_passed:
            logger.warning("Invalid password, username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        return user

    @abstractmethod
    async def _complete_login(
            self,
            request: Request,
            response: Response,
            user: User,
            options: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError(f"The {self.name!r} transport doesn't issue login credentials.")

    async def password_login(
            self,
            db: AsyncSession,
            form_data: OAuth2PasswordRequestForm,
            *,
            request: Request,
            response: Response,
            options: dict[str, Any],
    ) -> dict[str, Any]:
        user = await self._authenticate_password(
            db,
            form_data.username,
            form_data.password,
            request=request,
        )

        return await self._complete_login(
            request,
            response,
            user,
            options,
        )

    @abstractmethod
    async def authenticate(
            self,
            request: Request,
    ) -> Principal | None:
        raise NotImplementedError(f"The {self.name!r} transport doesn't implement authenticate method.")
