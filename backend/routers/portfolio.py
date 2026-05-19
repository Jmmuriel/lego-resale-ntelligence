from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.portfolio_engine import (
    PortfolioItem,
    PortfolioPosition,
    PortfolioStatus,
    PortfolioSummary,
    add_portfolio_item,
    delete_portfolio_item,
    get_portfolio_positions,
    get_portfolio_summary,
)


router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Check that the portfolio router is registered."""
    return {"router": "portfolio", "status": "ok"}


@router.get("", response_model=PortfolioSummary)
async def portfolio_summary() -> PortfolioSummary:
    """Return portfolio summary with current P&L."""
    return get_portfolio_summary()


@router.get("/positions", response_model=list[PortfolioPosition])
async def portfolio_positions() -> list[PortfolioPosition]:
    """Return open portfolio positions with current P&L."""
    return get_portfolio_positions()


class AddPositionBody(BaseModel):
    set_id: str
    set_name: str
    condition: str
    quantity: int = Field(ge=1)
    cost_basis_eur: float = Field(ge=0)
    purchased_at: date
    status: PortfolioStatus = "HOLDING"
    notes: str | None = None
    sell_target_eur: float | None = Field(default=None, ge=0)


@router.post("", response_model=PortfolioItem, status_code=201)
async def add_position(body: AddPositionBody) -> PortfolioItem:
    """Add a new portfolio position."""
    return add_portfolio_item(
        set_id=body.set_id,
        set_name=body.set_name,
        condition=body.condition,
        quantity=body.quantity,
        cost_basis_eur=body.cost_basis_eur,
        purchased_at=body.purchased_at,
        status=body.status,
        notes=body.notes,
        sell_target_eur=body.sell_target_eur,
    )


@router.delete("/{item_id}", response_model=dict)
async def delete_position(item_id: int) -> dict:
    """Delete a portfolio position by ID."""
    deleted = delete_portfolio_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Portfolio position {item_id} not found")
    return {"ok": True}
