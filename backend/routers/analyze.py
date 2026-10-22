import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from backend.security import LLM_BUDGET_DETAIL, limit_outbound_requests
from backend.services.price_engine import compute_anomaly_score, compute_fair_price
from src.capture import MAX_URL_LENGTH, UnsupportedListingURLError
from src.limits import LLMBudgetExceeded
from src.models import ListingAnalysis
from src.pipeline import PipelineError, analyze_listing_url
from src.placeholders import mock_analyze_listing


log = logging.getLogger(__name__)

router = APIRouter()

DEMO_LISTING_URL = "https://www.ebay.es/itm/demo-lego-75192"
UNSUPPORTED_URL_DETAIL = (
    "Only https listing URLs from eBay, Wallapop or Vinted can be analyzed. "
    "Paste a public listing link from one of those marketplaces."
)
# PipelineError messages are Spanish (shared with the Streamlit app); the V2 UI is English.
ANALYSIS_FAILED_DETAIL = (
    "Could not analyze this listing. It may be unavailable, missing a price, or a set "
    "outside the local catalog. Try another listing or use the no-cost demo opportunity."
)


class AnalyzeListingRequest(BaseModel):
    """Payload for on-demand listing analysis."""

    model_config = ConfigDict(str_strip_whitespace=True)

    url: str = Field(min_length=1, max_length=MAX_URL_LENGTH)


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


@router.post(
    "",
    response_model=AnalyzeListingResponse,
    dependencies=[Depends(limit_outbound_requests)],
)
def analyze_listing(request: AnalyzeListingRequest) -> AnalyzeListingResponse:
    """Analyze one listing URL and enrich it with V2 market context."""
    if request.url == DEMO_LISTING_URL:
        # Not a real listing: never fetch it or send it to the LLM.
        return analyze_demo_listing()

    try:
        analysis = analyze_listing_url(request.url)
    except UnsupportedListingURLError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=UNSUPPORTED_URL_DETAIL) from exc
    except LLMBudgetExceeded as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=LLM_BUDGET_DETAIL,
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    except PipelineError as exc:
        log.info("Listing analysis failed: %s", exc)
        raise HTTPException(status_code=422, detail=ANALYSIS_FAILED_DETAIL) from exc

    return AnalyzeListingResponse(
        **analysis.model_dump(),
        market_context=_build_market_context(analysis),
    )


@router.post("/demo", response_model=AnalyzeListingResponse)
def analyze_demo_listing() -> AnalyzeListingResponse:
    """Return a deterministic demo analysis without calling Anthropic or external marketplaces."""
    analysis = mock_analyze_listing(DEMO_LISTING_URL)

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
