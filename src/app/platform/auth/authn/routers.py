from typing import Any

from fastapi import APIRouter, Request, Response

from app.platform.auth.authn.co_authn import get_co_authn
from app.platform.auth.authn.dependency import OAuth2FormDep
from app.platform.auth.authn.exceptions import ForbiddenException
from app.platform.dependency import AsyncSessionDep
from app.platform.logging import get_logger
from app.platform.util.http import is_cross_site

logger = get_logger(__name__)

co_authn = get_co_authn()

router = APIRouter(tags=["authentication"])


@router.post("/login")
async def login(
        request: Request,
        response: Response,
        form_data: OAuth2FormDep,
        db: AsyncSessionDep,
) -> dict[str, Any]:
    """Login endpoint to get session cookies."""
    if is_cross_site(request):
        raise ForbiddenException("Cross-site login are not allowed.")

    return await co_authn.password_login(request, response)
