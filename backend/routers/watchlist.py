from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict

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


class WatchlistStatusUpdate(BaseModel):
    """Payload for changing a saved listing status."""

    status: str


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the watchlist router is registered."""
    return {"router": "watchlist", "status": "ok"}


@router.get("", response_model=list[WatchlistRecord])
async def list_watchlist(limit: int = Query(default=20, ge=1, le=100)) -> list[ListingAnalysisRecord]:
    """Return recent saved listing analyses."""
    return list_recent_listings(limit=limit)


@router.post("", response_model=WatchlistRecord, status_code=status.HTTP_201_CREATED)
async def create_watchlist_record(
    analysis: ListingAnalysis,
    listing_status: str = Query(default="watching"),
) -> ListingAnalysisRecord:
    """Save an analyzed listing into the shared V1/V2 watchlist."""
    try:
        return save_listing_analysis(analysis, status=listing_status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch("/{listing_id}/status", response_model=WatchlistRecord)
async def change_watchlist_status(
    listing_id: int,
    payload: WatchlistStatusUpdate,
) -> ListingAnalysisRecord:
    """Move a saved listing through the resale workflow."""
    try:
        record = update_listing_status(listing_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if record is None:
        raise HTTPException(status_code=404, detail="Watchlist record not found.")

    return record
