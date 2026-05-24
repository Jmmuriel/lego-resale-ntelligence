from fastapi import APIRouter, Query

from backend.services.data_quality import (
    ActiveCatalogEvidence,
    CatalogCandidate,
    DataQualityReport,
    get_data_quality_report,
    list_active_catalog_evidence,
    list_catalog_candidates,
)
from backend.services.price_engine import (
    FairPrice,
    PriceChange,
    PriceSnapshot,
    SetIntelligence,
    compute_fair_price,
    get_price_changes,
    get_recent_snapshots,
    get_set_intelligence,
)


router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the market router is registered."""
    return {"router": "market", "status": "ok"}


@router.get("/price/{set_id}", response_model=FairPrice)
async def market_price(
    set_id: str,
    condition: str = Query(default="USED_COMPLETE"),
) -> FairPrice:
    """Return dynamic fair price for one set and condition."""
    return compute_fair_price(set_id=set_id, condition=condition)


@router.get("/set/{set_id}", response_model=SetIntelligence)
async def set_intelligence(
    set_id: str,
    days: int = Query(default=180, ge=1, le=365),
) -> SetIntelligence:
    """Return compact market intelligence for one LEGO set."""
    return get_set_intelligence(set_id=set_id, days=days)


@router.get("/history/{set_id}", response_model=list[PriceSnapshot])
async def set_price_history(
    set_id: str,
    condition: str = Query(default="USED_COMPLETE"),
    days: int = Query(default=180, ge=1, le=365),
) -> list[PriceSnapshot]:
    """Return recent price snapshots for one set and condition."""
    return get_recent_snapshots(set_id=set_id, condition=condition, days=days)


@router.get("/trends", response_model=list[PriceChange])
async def market_trends(days: int = Query(default=90, ge=1, le=365)) -> list[PriceChange]:
    """Return strongest price changes from the curated seed history."""
    return get_price_changes(days=days)


@router.get("/data-quality", response_model=DataQualityReport)
async def market_data_quality() -> DataQualityReport:
    """Return V2 data maturity and validation metrics."""
    return get_data_quality_report()


@router.get("/catalog-candidates", response_model=list[CatalogCandidate])
async def market_catalog_candidates() -> list[CatalogCandidate]:
    """Return catalog candidates that are not active market data yet."""
    return list_catalog_candidates()


@router.get("/active-evidence", response_model=list[ActiveCatalogEvidence])
async def market_active_evidence() -> list[ActiveCatalogEvidence]:
    """Return active catalog evidence audits and blockers."""
    return list_active_catalog_evidence()
