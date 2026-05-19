import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.db.database import get_session_factory
from backend.db.models import PortfolioItem as PortfolioItemRecord
from backend.services.price_engine import compute_fair_price, get_price_changes


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PORTFOLIO_PATH = PROJECT_ROOT / "data" / "portfolio_seed.json"
FEES_RATE = 0.10
SHIPPING_OUT_EUR = 8.0

PortfolioStatus = Literal["HOLDING", "LISTED", "SOLD"]
HoldSellSignal = Literal["HOLD", "NEUTRAL", "SELL"]


class PortfolioItem(BaseModel):
    """One owned or demo portfolio position."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int
    set_id: str
    set_name: str
    condition: str
    quantity: int = Field(ge=1)
    cost_basis_eur: float = Field(ge=0)
    purchased_at: date
    status: PortfolioStatus
    notes: str | None = None
    sell_target_eur: float | None = Field(default=None, ge=0)


class PositionPnL(BaseModel):
    """Financial state of one portfolio position."""

    cost_basis_eur: float
    current_fair_value_eur: float
    net_if_sold_eur: float
    unrealized_pnl_eur: float
    unrealized_pnl_pct: float
    annualized_return_pct: float
    days_held: int
    price_confidence: Literal["HIGH", "MEDIUM", "LOW", "NONE"]
    hold_sell_signal: HoldSellSignal
    hold_sell_reason: str


class PortfolioPosition(BaseModel):
    """Portfolio item enriched with current P&L."""

    item: PortfolioItem
    pnl: PositionPnL


class PortfolioSummary(BaseModel):
    """Portfolio rollup for the V2 dashboard."""

    total_cost_basis_eur: float
    total_current_fair_value_eur: float
    total_net_if_sold_eur: float
    total_unrealized_pnl_eur: float
    total_unrealized_pnl_pct: float
    open_positions: int
    dominant_signal: HoldSellSignal
    top_position_id: int | None = None
    worst_position_id: int | None = None
    positions: list[PortfolioPosition]


def load_portfolio_items_from_json(path: Path = DEFAULT_PORTFOLIO_PATH) -> list[PortfolioItem]:
    """Load seed portfolio positions from JSON."""
    raw_items = json.loads(path.read_text(encoding="utf-8"))
    return [PortfolioItem.model_validate(item) for item in raw_items]


def load_portfolio_items_from_db(database_url: str | None = None) -> list[PortfolioItem]:
    """Load portfolio positions from the V2 database."""
    try:
        session_factory = (
            get_session_factory(database_url)
            if database_url is not None
            else get_session_factory()
        )
        with session_factory() as session:
            statement = select(PortfolioItemRecord).order_by(PortfolioItemRecord.id)
            records = session.scalars(statement).all()
    except SQLAlchemyError:
        return []

    return [
        PortfolioItem(
            id=record.id,
            set_id=record.set_id,
            set_name=record.set_name,
            condition=record.condition,
            quantity=record.quantity,
            cost_basis_eur=record.cost_basis_eur,
            purchased_at=record.purchased_at,
            status=record.status,
            notes=record.notes,
            sell_target_eur=record.sell_target_eur,
        )
        for record in records
    ]


def load_portfolio_items(
    path: Path = DEFAULT_PORTFOLIO_PATH,
    prefer_db: bool = True,
) -> list[PortfolioItem]:
    """Load portfolio positions from DB first, then JSON as a local fallback."""
    if prefer_db:
        db_items = load_portfolio_items_from_db()
        if db_items:
            return db_items

    return load_portfolio_items_from_json(path)


def compute_position_pnl(
    item: PortfolioItem,
    as_of: date | None = None,
) -> PositionPnL:
    """Compute current value and unrealized P&L for one position."""
    reference_date = as_of or datetime.now(timezone.utc).date()
    fair_price = compute_fair_price(
        set_id=item.set_id,
        condition=item.condition,
        as_of=reference_date,
    )
    unit_fair_value = fair_price.avg_eur if fair_price.avg_eur is not None else item.cost_basis_eur / item.quantity
    current_fair_value = round(unit_fair_value * item.quantity, 2)
    net_if_sold = round(current_fair_value * (1 - FEES_RATE) - (SHIPPING_OUT_EUR * item.quantity), 2)
    unrealized_pnl = round(net_if_sold - item.cost_basis_eur, 2)
    unrealized_pnl_pct = (
        round((unrealized_pnl / item.cost_basis_eur) * 100, 2)
        if item.cost_basis_eur > 0
        else 0.0
    )
    days_held = max((reference_date - item.purchased_at).days, 0)
    annualized_return_pct = (
        round((unrealized_pnl_pct / days_held) * 365, 2)
        if days_held > 0
        else 0.0
    )
    trend_direction = _trend_direction(item.set_id, item.condition, as_of=reference_date)
    signal, reason = compute_hold_sell_signal(
        unrealized_pnl_pct=unrealized_pnl_pct,
        trend_direction=trend_direction,
        days_held=days_held,
        price_confidence=fair_price.confidence,
    )

    return PositionPnL(
        cost_basis_eur=round(item.cost_basis_eur, 2),
        current_fair_value_eur=current_fair_value,
        net_if_sold_eur=net_if_sold,
        unrealized_pnl_eur=unrealized_pnl,
        unrealized_pnl_pct=unrealized_pnl_pct,
        annualized_return_pct=annualized_return_pct,
        days_held=days_held,
        price_confidence=fair_price.confidence,
        hold_sell_signal=signal,
        hold_sell_reason=reason,
    )


def compute_hold_sell_signal(
    unrealized_pnl_pct: float,
    trend_direction: str,
    days_held: int,
    price_confidence: str,
) -> tuple[HoldSellSignal, str]:
    """Compute a transparent hold/sell signal."""
    if price_confidence == "NONE":
        return "NEUTRAL", "Sin precio dinámico suficiente; revisar manualmente antes de decidir."

    if unrealized_pnl_pct >= 25 and days_held >= 90:
        return "SELL", "Ganancia estimada fuerte y holding suficiente; considerar realizar beneficio."

    if trend_direction == "UP" and unrealized_pnl_pct >= 0:
        return "HOLD", "Tendencia reciente positiva; puede compensar esperar."

    if trend_direction == "DOWN" and days_held >= 120:
        return "SELL", "Tendencia reciente negativa y holding prolongado; revisar salida."

    if unrealized_pnl_pct <= -10:
        return "NEUTRAL", "Pérdida estimada relevante; evitar venta impulsiva sin revisar mercado."

    return "NEUTRAL", "Señal mixta; mantener en seguimiento."


def get_portfolio_positions(
    as_of: date | None = None,
    items: list[PortfolioItem] | None = None,
) -> list[PortfolioPosition]:
    """Return open portfolio positions enriched with P&L."""
    portfolio_items = load_portfolio_items() if items is None else items
    return [
        PortfolioPosition(
            item=item,
            pnl=compute_position_pnl(item, as_of=as_of),
        )
        for item in portfolio_items
        if item.status != "SOLD"
    ]


def get_portfolio_summary(
    as_of: date | None = None,
    items: list[PortfolioItem] | None = None,
) -> PortfolioSummary:
    """Build a portfolio summary from current positions."""
    positions = get_portfolio_positions(as_of=as_of, items=items)
    total_cost = round(sum(position.pnl.cost_basis_eur for position in positions), 2)
    total_current = round(sum(position.pnl.current_fair_value_eur for position in positions), 2)
    total_net_if_sold = round(sum(position.pnl.net_if_sold_eur for position in positions), 2)
    total_pnl = round(sum(position.pnl.unrealized_pnl_eur for position in positions), 2)
    total_pnl_pct = round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0.0

    top_position = max(positions, key=lambda position: position.pnl.unrealized_pnl_eur, default=None)
    worst_position = min(positions, key=lambda position: position.pnl.unrealized_pnl_eur, default=None)

    return PortfolioSummary(
        total_cost_basis_eur=total_cost,
        total_current_fair_value_eur=total_current,
        total_net_if_sold_eur=total_net_if_sold,
        total_unrealized_pnl_eur=total_pnl,
        total_unrealized_pnl_pct=total_pnl_pct,
        open_positions=len(positions),
        dominant_signal=_dominant_signal(positions),
        top_position_id=top_position.item.id if top_position else None,
        worst_position_id=worst_position.item.id if worst_position else None,
        positions=positions,
    )


def add_portfolio_item(
    set_id: str,
    set_name: str,
    condition: str,
    quantity: int,
    cost_basis_eur: float,
    purchased_at: date,
    status: PortfolioStatus = "HOLDING",
    notes: str | None = None,
    sell_target_eur: float | None = None,
) -> PortfolioItem:
    """Add a new portfolio position, persisting to DB if available or JSON file."""
    try:
        from backend.db.models import PortfolioItem as PortfolioItemRecord  # noqa: PLC0415

        session_factory = get_session_factory()
        with session_factory() as session:
            record = PortfolioItemRecord(
                set_id=set_id,
                set_name=set_name,
                condition=condition,
                quantity=quantity,
                cost_basis_eur=cost_basis_eur,
                purchased_at=purchased_at,
                status=status,
                notes=notes,
                sell_target_eur=sell_target_eur,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return PortfolioItem(
                id=record.id,
                set_id=record.set_id,
                set_name=record.set_name,
                condition=record.condition,
                quantity=record.quantity,
                cost_basis_eur=record.cost_basis_eur,
                purchased_at=record.purchased_at,
                status=record.status,
                notes=record.notes,
                sell_target_eur=record.sell_target_eur,
            )
    except Exception:
        raw = json.loads(DEFAULT_PORTFOLIO_PATH.read_text(encoding="utf-8"))
        new_id = max((item["id"] for item in raw), default=0) + 1
        new_item = {
            "id": new_id,
            "set_id": set_id,
            "set_name": set_name,
            "condition": condition,
            "quantity": quantity,
            "cost_basis_eur": cost_basis_eur,
            "purchased_at": purchased_at.isoformat(),
            "status": status,
            "notes": notes,
            "sell_target_eur": sell_target_eur,
        }
        raw.append(new_item)
        DEFAULT_PORTFOLIO_PATH.write_text(
            json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return PortfolioItem.model_validate(new_item)


def delete_portfolio_item(item_id: int) -> bool:
    """Delete a portfolio position by ID. Returns True if found and deleted."""
    try:
        from backend.db.models import PortfolioItem as PortfolioItemRecord  # noqa: PLC0415

        session_factory = get_session_factory()
        with session_factory() as session:
            record = session.get(PortfolioItemRecord, item_id)
            if record is None:
                return False
            session.delete(record)
            session.commit()
            return True
    except Exception:
        raw = json.loads(DEFAULT_PORTFOLIO_PATH.read_text(encoding="utf-8"))
        before = len(raw)
        raw = [item for item in raw if item["id"] != item_id]
        if len(raw) == before:
            return False
        DEFAULT_PORTFOLIO_PATH.write_text(
            json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return True


def _trend_direction(set_id: str, condition: str, as_of: date) -> str:
    changes = get_price_changes(days=90, as_of=as_of)
    for change in changes:
        if change.set_id == set_id and change.condition == condition:
            if change.change_pct >= 0.03:
                return "UP"
            if change.change_pct <= -0.03:
                return "DOWN"
    return "FLAT"


def _dominant_signal(positions: list[PortfolioPosition]) -> HoldSellSignal:
    signal_order: list[HoldSellSignal] = ["SELL", "HOLD", "NEUTRAL"]
    counts = {
        signal: sum(1 for position in positions if position.pnl.hold_sell_signal == signal)
        for signal in signal_order
    }
    return max(signal_order, key=lambda signal: counts[signal])
