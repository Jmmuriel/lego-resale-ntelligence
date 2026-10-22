import logging
import os

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routers import analyze, briefings, market, portfolio, watchlist
from backend.security import BodySizeLimitMiddleware, demo_writes_allowed
from src.limits import env_flag


log = logging.getLogger(__name__)

APP_TITLE = "LEGO Resale Intelligence API"
APP_VERSION = "0.1.0"
# Used only when BACKEND_CORS_ORIGINS is unset. Local origins (localhost:3000)
# must be listed explicitly, as .env.example and scripts/v2_start_api.sh do.
PUBLIC_CORS_ORIGINS = ["https://lego-resale-ntelligence.vercel.app"]
CORS_METHODS = ["GET", "POST"]
# Only offered to browsers when the demo accepts writes (LRI_DEMO_ALLOW_WRITES=1).
WRITE_METHODS = ["PATCH", "DELETE"]
CORS_HEADERS = ["Content-Type"]
INTERNAL_ERROR_DETAIL = "Internal server error."


def create_app() -> FastAPI:
    """Create the FastAPI app for the V2 backend."""
    docs_enabled = env_flag("LRI_ENABLE_DOCS")
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description="V2 API for LEGO resale market intelligence.",
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )

    # Added before CORS so CORS stays the outermost layer and its 413s carry CORS headers.
    app.add_middleware(BodySizeLimitMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_get_cors_origins(),
        allow_credentials=False,
        allow_methods=CORS_METHODS + (WRITE_METHODS if demo_writes_allowed() else []),
        allow_headers=CORS_HEADERS,
    )
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)

    app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
    app.include_router(market.router, prefix="/api/market", tags=["market"])
    app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
    app.include_router(briefings.router, prefix="/api/briefings", tags=["briefings"])
    app.include_router(watchlist.router, prefix="/api/watchlist", tags=["watchlist"])

    return app


def _get_cors_origins() -> list[str]:
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS", "")
    configured = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if configured:
        return configured
    return list(PUBLIC_CORS_ORIGINS)


async def _validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """FastAPI's 422 shape without echoing the submitted value.

    The echoed input can be huge, or Infinity/NaN, which is not valid JSON.
    """
    errors = [{key: value for key, value in error.items() if key != "input"} for error in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": jsonable_encoder(errors)})


async def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Log unexpected errors server-side and return a generic message to the client."""
    log.error("Unhandled error on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": INTERNAL_ERROR_DETAIL})


app = create_app()


@app.get("/health")
async def health() -> dict[str, str]:
    """Return a minimal health check for deploy and local verification."""
    return {"status": "ok", "service": "lego-resale-intelligence-api"}
