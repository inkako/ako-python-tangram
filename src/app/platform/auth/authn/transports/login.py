from typing import Any

from fastapi import Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.auth.authn.core import Transport


async def password_login(
        transport: Transport,
        *,
        db: AsyncSession,
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestForm,
) -> dict[str, Any]:
    user = await transport.runtime.authenticate_password(
        db,
        form_data.username,
        form_data.password,
        request=request,
    )

    return await transport.complete_login(
        request,
        response,
        user,
    )
