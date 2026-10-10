from app.platform.dependency.dependencies import OAuth2FormDep, AsyncSessionDep
from starlette.requests import Request
from starlette.responses import Response


async def login(
        request: Request,
        response: Response,
        form_data: OAuth2FormDep,
        db: AsyncSessionDep,
):
    ...
