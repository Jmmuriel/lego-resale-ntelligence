"""Guards for the public demo API: read-only switch, body size cap and per-client rate limits."""

import ipaddress

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.limits import DAY_SECONDS, FixedWindowLimiter, env_flag, env_int


READ_ONLY_DETAIL = "This public demo is read-only."
BODY_TOO_LARGE_DETAIL = "Request body too large."
RATE_LIMIT_DETAIL = (
    "Too many analysis requests. Please try again later, "
    "or use the no-cost demo opportunity."
)
LLM_BUDGET_DETAIL = (
    "The live analyzer has reached its daily limit. "
    "Please try again tomorrow or use the no-cost demo opportunity."
)

DEFAULT_RATE_LIMIT_PER_MINUTE = 10
DEFAULT_RATE_LIMIT_PER_DAY = 60
# The largest legitimate body, a watchlist ListingAnalysis, is a few KB.
DEFAULT_MAX_BODY_BYTES = 65_536

_outbound_limiter = FixedWindowLimiter()


class RequestBodyTooLarge(HTTPException):
    """Raised while reading a request body that passes LRI_MAX_BODY_BYTES.

    It is an HTTPException so FastAPI re-raises it from body parsing (instead of
    turning it into a 400) and the app's HTTPException handler answers 413.
    """

    def __init__(self) -> None:
        super().__init__(status_code=413, detail=BODY_TOO_LARGE_DETAIL)


class BodySizeLimitMiddleware:
    """Refuse request bodies over LRI_MAX_BODY_BYTES with 413.

    Pure ASGI, so it runs before FastAPI buffers and parses the body, and so
    before the read-only check and the rate limiter, which are route
    dependencies. A declared Content-Length over the limit is refused without
    reading anything; a chunked body is counted as it arrives and refused as
    soon as it passes the limit.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        max_bytes = env_int("LRI_MAX_BODY_BYTES", DEFAULT_MAX_BODY_BYTES, minimum=1)
        declared_length = _content_length(scope)
        if declared_length is not None and declared_length > max_bytes:
            response = JSONResponse(status_code=413, content={"detail": BODY_TOO_LARGE_DETAIL})
            await response(scope, receive, send)
            return

        received = 0

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > max_bytes:
                    raise RequestBodyTooLarge()
            return message

        await self.app(scope, limited_receive, send)


def _content_length(scope: Scope) -> int | None:
    for name, value in scope.get("headers", []):
        if name == b"content-length":
            try:
                return int(value)
            except ValueError:
                return None
    return None


def demo_writes_allowed() -> bool:
    """Writes to shared demo data are off unless LRI_DEMO_ALLOW_WRITES=1."""
    return env_flag("LRI_DEMO_ALLOW_WRITES")


def require_demo_writes() -> None:
    """Dependency for every route that changes shared data."""
    if not demo_writes_allowed():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=READ_ONLY_DETAIL)


def limit_outbound_requests(request: Request) -> None:
    """Dependency for routes that fetch external pages or may call the paid LLM.

    Limits each client to LRI_RATE_LIMIT_PER_MINUTE and LRI_RATE_LIMIT_PER_DAY
    requests (fixed windows, in process memory).
    """
    per_minute = env_int("LRI_RATE_LIMIT_PER_MINUTE", DEFAULT_RATE_LIMIT_PER_MINUTE)
    per_day = env_int("LRI_RATE_LIMIT_PER_DAY", DEFAULT_RATE_LIMIT_PER_DAY)
    retry_after = _outbound_limiter.hit(
        client_key(request),
        [(per_minute, 60), (per_day, DAY_SECONDS)],
    )
    if retry_after is not None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=RATE_LIMIT_DETAIL,
            headers={"Retry-After": str(retry_after)},
        )


def client_key(request: Request) -> str:
    """Rate-limit key for the caller.

    Behind Railway, uvicorn's proxy-headers support sets request.client from
    X-Forwarded-For (see scripts/v2_boot_api.sh). IPv6 clients are grouped by
    /64, since one host usually controls a whole /64.
    """
    host = request.client.host if request.client else ""
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return host or "unknown"

    if ip.version == 6:
        if ip.ipv4_mapped is not None:
            return str(ip.ipv4_mapped)
        return str(ipaddress.ip_network(f"{ip}/64", strict=False))

    return str(ip)


def reset_rate_limits() -> None:
    _outbound_limiter.reset()
