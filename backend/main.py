import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import analyze, briefings, market, portfolio, watchlist


APP_TITLE = "LEGO Resale Intelligence API"
APP_VERSION = "0.1.0"
DEFAULT_CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]


def create_app() -> FastAPI:
    """Create the FastAPI app for the V2 backend."""
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description="V2 API for LEGO resale market intelligence.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
    app.include_router(market.router, prefix="/api/market", tags=["market"])
    app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
    app.include_router(briefings.router, prefix="/api/briefings", tags=["briefings"])
    app.include_router(watchlist.router, prefix="/api/watchlist", tags=["watchlist"])

    return app


def _get_cors_origins() -> list[str]:
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS", "")
    configured = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return configured or DEFAULT_CORS_ORIGINS


app = create_app()


@app.get("/health")
async def health() -> dict[str, str]:
    """Return a minimal health check for deploy and local verification."""
    return {"status": "ok", "service": "lego-resale-intelligence-api"}
