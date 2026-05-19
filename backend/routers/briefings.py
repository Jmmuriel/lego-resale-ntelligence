from fastapi import APIRouter, Query

from backend.services.ai_analyst import (
    MarketBriefing,
    generate_briefing,
    generate_briefing_with_llm,
    get_latest_briefings,
)


router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the briefings router is registered."""
    return {"router": "briefings", "status": "ok"}


@router.get("", response_model=list[MarketBriefing])
async def list_briefings(limit: int = Query(default=1, ge=1, le=10)) -> list[MarketBriefing]:
    """Return latest market briefings."""
    return get_latest_briefings(limit=limit)


@router.post("/generate", response_model=MarketBriefing)
async def create_briefing(
    period_days: int = Query(default=7, ge=1, le=90),
    use_llm: bool = Query(default=True, description="Use Claude Sonnet if API key is set"),
) -> MarketBriefing:
    """Generate a market briefing. Uses Claude Sonnet when ANTHROPIC_API_KEY is set."""
    if use_llm:
        return generate_briefing_with_llm(period_days=period_days)
    return generate_briefing(period_days=period_days)
