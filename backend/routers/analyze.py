from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.services.price_engine import compute_anomaly_score, compute_fair_price
from src.models import ListingAnalysis
from src.pipeline import PipelineError, analyze_listing_url
from src.placeholders import mock_analyze_listing


router = APIRouter()


class AnalyzeListingRequest(BaseModel):
    """Payload for on-demand listing analysis."""

    model_config = ConfigDict(str_strip_whitespace=True)

    url: str = Field(min_length=1)


class AnalyzeMarketContext(BaseModel):
    """V2 market context added on top of the V1 listing analysis."""

    fair_price_eur: float | None = None
    fair_price_source: Literal["dynamic_history", "manual_reference", "unavailable"]
    price_confidence: Literal["HIGH", "MEDIUM", "LOW", "NONE"]
    anomaly_score: float | None = None
    snapshot_count: int = 0
    days_since_update: int | None = None


class AnalyzeListingResponse(ListingAnalysis):
    """V2 response for listing analysis with market context."""

    market_context: AnalyzeMarketContext


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the analyze router is registered."""
    return {"router": "analyze", "status": "ok"}


@router.post("", response_model=AnalyzeListingResponse)
async def analyze_listing(request: AnalyzeListingRequest) -> AnalyzeListingResponse:
    """Analyze one listing URL and enrich it with V2 market context."""
    try:
        analysis = analyze_listing_url(request.url)
    except PipelineError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return AnalyzeListingResponse(
        **analysis.model_dump(),
        market_context=_build_market_context(analysis),
    )


@router.post("/demo", response_model=AnalyzeListingResponse)
async def analyze_demo_listing() -> AnalyzeListingResponse:
    """Return a deterministic demo analysis without calling Anthropic or external marketplaces."""
    analysis = mock_analyze_listing("https://www.ebay.es/itm/demo-lego-75192")

    return AnalyzeListingResponse(
        **analysis.model_dump(),
        market_context=_build_market_context(analysis),
    )


def _build_market_context(analysis: ListingAnalysis) -> AnalyzeMarketContext:
    """Build dynamic pricing context while keeping the V1 analysis unchanged."""
    if not analysis.set_id or not analysis.condition:
        return AnalyzeMarketContext(
            fair_price_eur=analysis.fair_price_eur,
            fair_price_source="unavailable",
            price_confidence="NONE",
        )

    dynamic_fair_price = compute_fair_price(
        set_id=analysis.set_id,
        condition=analysis.condition,
    )

    if dynamic_fair_price.avg_eur is not None:
        return AnalyzeMarketContext(
            fair_price_eur=dynamic_fair_price.avg_eur,
            fair_price_source="dynamic_history",
            price_confidence=dynamic_fair_price.confidence,
            anomaly_score=_safe_anomaly_score(
                asking_price_eur=analysis.asking_price_eur,
                fair_price_eur=dynamic_fair_price.avg_eur,
            ),
            snapshot_count=dynamic_fair_price.snapshot_count,
            days_since_update=dynamic_fair_price.days_since_update,
        )

    return AnalyzeMarketContext(
        fair_price_eur=analysis.fair_price_eur,
        fair_price_source="manual_reference" if analysis.fair_price_eur is not None else "unavailable",
        price_confidence="NONE",
        anomaly_score=_safe_anomaly_score(
            asking_price_eur=analysis.asking_price_eur,
            fair_price_eur=analysis.fair_price_eur,
        ),
    )


def _safe_anomaly_score(
    asking_price_eur: float | None,
    fair_price_eur: float | None,
) -> float | None:
    if asking_price_eur is None:
        return None

    return compute_anomaly_score(
        asking_price_eur=asking_price_eur,
        fair_avg_eur=fair_price_eur,
    )
