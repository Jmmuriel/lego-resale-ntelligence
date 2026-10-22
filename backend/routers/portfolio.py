from datetime import date, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.security import require_demo_writes
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
def portfolio_summary() -> PortfolioSummary:
    """Return portfolio summary with current P&L."""
    return get_portfolio_summary()


@router.get("/positions", response_model=list[PortfolioPosition])
def portfolio_positions() -> list[PortfolioPosition]:
    """Return open portfolio positions with current P&L."""
    return get_portfolio_positions()


EARLIEST_PURCHASE_DATE = date(1990, 1, 1)
MAX_PRICE_EUR = 100_000


class AddPositionBody(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, allow_inf_nan=False)

    set_id: str = Field(pattern=r"^\d{4,6}(-\d{1,2})?$", max_length=20)
    set_name: str = Field(min_length=1, max_length=120)
    condition: Literal["SEALED", "USED_COMPLETE", "USED_INCOMPLETE", "UNKNOWN"]
    quantity: int = Field(ge=1, le=100)
    cost_basis_eur: float = Field(ge=0, le=MAX_PRICE_EUR)
    purchased_at: date
    status: PortfolioStatus = "HOLDING"
    notes: str | None = Field(default=None, max_length=500)
    sell_target_eur: float | None = Field(default=None, ge=0, le=MAX_PRICE_EUR)

    @field_validator("purchased_at")
    @classmethod
    def validate_purchased_at(cls, value: date) -> date:
        # One day of slack: the browser sends its UTC date.
        if not EARLIEST_PURCHASE_DATE <= value <= date.today() + timedelta(days=1):
            raise ValueError("purchased_at must be between 1990-01-01 and today.")
        return value


@router.post(
    "",
    response_model=PortfolioItem,
    status_code=201,
    dependencies=[Depends(require_demo_writes)],
)
def add_position(body: AddPositionBody) -> PortfolioItem:
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


@router.delete("/{item_id}", response_model=dict, dependencies=[Depends(require_demo_writes)])
def delete_position(item_id: int = Path(ge=1, le=2_147_483_647)) -> dict:
    """Delete a portfolio position by ID."""
    deleted = delete_portfolio_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Portfolio position {item_id} not found")
    return {"ok": True}
