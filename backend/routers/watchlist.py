from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field

from backend.security import require_demo_writes
from src.capture import MAX_URL_LENGTH
from src.db import (
    ListingAnalysisRecord,
    list_recent_listings,
    save_listing_analysis,
    update_listing_status,
)
from src.models import ListingAnalysis


router = APIRouter()


class WatchlistRecord(BaseModel):
    """API shape for a saved listing analysis."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: str
    url: str
    marketplace: str | None = None
    set_id: str | None = None
    condition: str | None = None
    asking_price_eur: float | None = None
    shipping_eur: float | None = None
    fair_price_eur: float | None = None
    gross_margin_eur: float | None = None
    net_margin_eur: float | None = None
    opportunity_score: int | None = None
    category: str | None = None
    risk_flags: list[str]
    notes: str | None = None


WatchlistStatus = Literal["analyzed", "watching", "discarded", "bought"]
MAX_PRICE_EUR = 100_000


class WatchlistCreateBody(ListingAnalysis):
    """ListingAnalysis as sent by a client, with bounds on every stored field."""

    model_config = ConfigDict(str_strip_whitespace=True, allow_inf_nan=False)

    url: str = Field(min_length=1, max_length=MAX_URL_LENGTH)
    marketplace: str | None = Field(default=None, max_length=50)
    set_id: str | None = Field(default=None, max_length=20)
    asking_price_eur: float | None = Field(default=None, ge=0, le=MAX_PRICE_EUR)
    shipping_eur: float | None = Field(default=None, ge=0, le=MAX_PRICE_EUR)
    fair_price_eur: float | None = Field(default=None, ge=0, le=MAX_PRICE_EUR)
    gross_margin_eur: float | None = Field(default=None, ge=-MAX_PRICE_EUR, le=MAX_PRICE_EUR)
    net_margin_eur: float | None = Field(default=None, ge=-MAX_PRICE_EUR, le=MAX_PRICE_EUR)
    risk_flags: list[Annotated[str, Field(max_length=120)]] = Field(default_factory=list, max_length=20)
    notes: str | None = Field(default=None, max_length=1000)


class WatchlistStatusUpdate(BaseModel):
    """Payload for changing a saved listing status."""

    status: WatchlistStatus


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the watchlist router is registered."""
    return {"router": "watchlist", "status": "ok"}


@router.get("", response_model=list[WatchlistRecord])
def list_watchlist(limit: int = Query(default=20, ge=1, le=100)) -> list[ListingAnalysisRecord]:
    """Return recent saved listing analyses."""
    return list_recent_listings(limit=limit)


@router.post(
    "",
    response_model=WatchlistRecord,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_demo_writes)],
)
def create_watchlist_record(
    analysis: WatchlistCreateBody,
    listing_status: WatchlistStatus = Query(default="watching"),
) -> ListingAnalysisRecord:
    """Save an analyzed listing into the shared V1/V2 watchlist."""
    try:
        return save_listing_analysis(analysis, status=listing_status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch(
    "/{listing_id}/status",
    response_model=WatchlistRecord,
    dependencies=[Depends(require_demo_writes)],
)
def change_watchlist_status(
    payload: WatchlistStatusUpdate,
    listing_id: int = Path(ge=1, le=2_147_483_647),
) -> ListingAnalysisRecord:
    """Move a saved listing through the resale workflow."""
    try:
        record = update_listing_status(listing_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if record is None:
        raise HTTPException(status_code=404, detail="Watchlist record not found.")

    return record
