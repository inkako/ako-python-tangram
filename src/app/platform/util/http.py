from fastapi import Request


def is_cross_site(request: Request) -> bool:
    """Check whether the request is a cross-site request.

    Inspects the `sec-fetch-site` header:
    Returns True if the value is "cross-site",
    and False otherwise.

    Args:
        request: The FastAPI Request object.

    Returns:
        bool: True if the request is cross-site, False otherwise.
    """
    return request.headers.get("sec-fetch-site") == "cross-site"
