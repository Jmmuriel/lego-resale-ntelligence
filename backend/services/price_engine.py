import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.db.database import get_session_factory
from backend.db.models import PriceHistory as PriceHistoryRecord

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRICE_HISTORY_PATH = PROJECT_ROOT / "data" / "price_history_seed.json"
Confidence = Literal["HIGH", "MEDIUM", "LOW", "NONE"]


class PriceSnapshot(BaseModel):
    """One historical market price observation for a set and condition."""

    model_config = ConfigDict(str_strip_whitespace=True)

    set_id: str
    condition: str
    source: str
    price_min_eur: float = Field(ge=0)
    price_avg_eur: float = Field(ge=0)
    price_max_eur: float = Field(ge=0)
    sample_count: int = Field(ge=0)
    recorded_at: date


class FairPrice(BaseModel):
    """Dynamic fair price computed from historical snapshots."""

    set_id: str
    condition: str
    avg_eur: float | None = None
    min_eur: float | None = None
    max_eur: float | None = None
    confidence: Confidence
    sample_count: int = 0
    snapshot_count: int = 0
    days_since_update: int | None = None


class PriceChange(BaseModel):
    """Price movement for a set and condition over a period."""

    set_id: str
    condition: str
    start_avg_eur: float
    end_avg_eur: float
    change_eur: float
    change_pct: float


class SetIntelligence(BaseModel):
    """Market intelligence summary for one LEGO set."""

    set_id: str
    available_conditions: list[str]
    fair_prices: list[FairPrice]
    strongest_change: PriceChange | None = None
    market_signal: Literal["UP", "DOWN", "STABLE", "UNKNOWN"]
    summary: str


def load_price_snapshots_from_json(path: Path = DEFAULT_PRICE_HISTORY_PATH) -> list[PriceSnapshot]:
    """Load curated price snapshots from JSON seed data."""
    raw_snapshots = json.loads(path.read_text(encoding="utf-8"))
    return [PriceSnapshot.model_validate(snapshot) for snapshot in raw_snapshots]


def load_price_snapshots_from_db(database_url: str | None = None) -> list[PriceSnapshot]:
    """Load price snapshots from the V2 database."""
    try:
        session_factory = (
            get_session_factory(database_url)
            if database_url is not None
            else get_session_factory()
        )
        with session_factory() as session:
            statement = select(PriceHistoryRecord).order_by(
                PriceHistoryRecord.recorded_at,
                PriceHistoryRecord.id,
            )
            records = session.scalars(statement).all()
    except SQLAlchemyError:
        return []

    return [
        PriceSnapshot(
            set_id=record.set_id,
            condition=record.condition,
            source=record.source,
            price_min_eur=record.price_min_eur,
            price_avg_eur=record.price_avg_eur,
            price_max_eur=record.price_max_eur,
            sample_count=record.sample_count,
            recorded_at=record.recorded_at,
        )
        for record in records
    ]


def load_price_snapshots(
    path: Path = DEFAULT_PRICE_HISTORY_PATH,
    prefer_db: bool = True,
) -> list[PriceSnapshot]:
    """Load price snapshots from DB first, then JSON as a local fallback."""
    if prefer_db:
        db_snapshots = load_price_snapshots_from_db()
        if db_snapshots:
            return db_snapshots

    return load_price_snapshots_from_json(path)


def get_recent_snapshots(
    set_id: str,
    condition: str,
    days: int = 180,
    as_of: date | None = None,
    snapshots: list[PriceSnapshot] | None = None,
) -> list[PriceSnapshot]:
    """Return recent snapshots for one set and condition."""
    reference_date = as_of or datetime.now(timezone.utc).date()
    all_snapshots = load_price_snapshots() if snapshots is None else snapshots

    filtered = [
        snapshot
        for snapshot in all_snapshots
        if snapshot.set_id == set_id
        and snapshot.condition == condition
        and 0 <= (reference_date - snapshot.recorded_at).days <= days
    ]
    return sorted(filtered, key=lambda snapshot: snapshot.recorded_at)


def exponential_decay_weights(
    dates: list[date],
    as_of: date | None = None,
    half_life_days: float = 45.0,
) -> list[float]:
    """Calculate recency weights that sum to one."""
    if not dates:
        return []

    reference_date = as_of or max(dates)
    raw_weights = [
        0.5 ** (max((reference_date - snapshot_date).days, 0) / half_life_days)
        for snapshot_date in dates
    ]
    total_weight = sum(raw_weights)
    if total_weight == 0:
        return [1 / len(dates)] * len(dates)

    return [weight / total_weight for weight in raw_weights]


def compute_fair_price(
    set_id: str,
    condition: str,
    days: int = 180,
    as_of: date | None = None,
    snapshots: list[PriceSnapshot] | None = None,
) -> FairPrice:
    """Compute dynamic fair price from curated historical snapshots."""
    recent_snapshots = get_recent_snapshots(
        set_id=set_id,
        condition=condition,
        days=days,
        as_of=as_of,
        snapshots=snapshots,
    )

    if not recent_snapshots:
        return FairPrice(
            set_id=set_id,
            condition=condition,
            confidence="NONE",
        )

    reference_date = as_of or datetime.now(timezone.utc).date()
    weights = exponential_decay_weights(
        [snapshot.recorded_at for snapshot in recent_snapshots],
        as_of=reference_date,
    )
    weighted_avg = sum(
        snapshot.price_avg_eur * weight
        for snapshot, weight in zip(recent_snapshots, weights, strict=True)
    )
    latest_snapshot = recent_snapshots[-1]

    return FairPrice(
        set_id=set_id,
        condition=condition,
        avg_eur=round(weighted_avg, 2),
        min_eur=round(min(snapshot.price_min_eur for snapshot in recent_snapshots), 2),
        max_eur=round(max(snapshot.price_max_eur for snapshot in recent_snapshots), 2),
        confidence=_confidence_for_snapshot_count(len(recent_snapshots)),
        sample_count=sum(snapshot.sample_count for snapshot in recent_snapshots),
        snapshot_count=len(recent_snapshots),
        days_since_update=(reference_date - latest_snapshot.recorded_at).days,
    )


def compute_anomaly_score(asking_price_eur: float, fair_avg_eur: float | None) -> float | None:
    """Measure how far asking price is from fair price.

    Negative means cheaper than market. Positive means more expensive than market.
    """
    if fair_avg_eur is None or fair_avg_eur <= 0:
        return None

    return round((asking_price_eur - fair_avg_eur) / fair_avg_eur, 4)


def get_price_changes(
    days: int = 90,
    as_of: date | None = None,
    snapshots: list[PriceSnapshot] | None = None,
) -> list[PriceChange]:
    """Return strongest price movements in the selected period."""
    reference_date = as_of or datetime.now(timezone.utc).date()
    all_snapshots = load_price_snapshots() if snapshots is None else snapshots
    grouped: dict[tuple[str, str], list[PriceSnapshot]] = {}

    for snapshot in all_snapshots:
        age_days = (reference_date - snapshot.recorded_at).days
        if 0 <= age_days <= days:
            grouped.setdefault((snapshot.set_id, snapshot.condition), []).append(snapshot)

    changes = []
    for (set_id, condition), group in grouped.items():
        ordered = sorted(group, key=lambda snapshot: snapshot.recorded_at)
        if len(ordered) < 2:
            continue

        start_avg = ordered[0].price_avg_eur
        end_avg = ordered[-1].price_avg_eur
        if start_avg <= 0:
            continue

        change_eur = end_avg - start_avg
        changes.append(
            PriceChange(
                set_id=set_id,
                condition=condition,
                start_avg_eur=round(start_avg, 2),
                end_avg_eur=round(end_avg, 2),
                change_eur=round(change_eur, 2),
                change_pct=round(change_eur / start_avg, 4),
            )
        )

    return sorted(changes, key=lambda change: abs(change.change_pct), reverse=True)


def get_set_intelligence(
    set_id: str,
    days: int = 180,
    as_of: date | None = None,
    snapshots: list[PriceSnapshot] | None = None,
) -> SetIntelligence:
    """Build a compact intelligence view for one set across known conditions."""
    all_snapshots = load_price_snapshots() if snapshots is None else snapshots
    matching_snapshots = [snapshot for snapshot in all_snapshots if snapshot.set_id == set_id]
    conditions = sorted({snapshot.condition for snapshot in matching_snapshots})
    fair_prices = [
        compute_fair_price(
            set_id=set_id,
            condition=condition,
            days=days,
            as_of=as_of,
            snapshots=all_snapshots,
        )
        for condition in conditions
    ]
    changes = [
        change
        for change in get_price_changes(days=days, as_of=as_of, snapshots=all_snapshots)
        if change.set_id == set_id
    ]
    strongest_change = changes[0] if changes else None

    if strongest_change is None:
        market_signal: Literal["UP", "DOWN", "STABLE", "UNKNOWN"] = (
            "UNKNOWN" if not fair_prices else "STABLE"
        )
    elif strongest_change.change_pct >= 0.03:
        market_signal = "UP"
    elif strongest_change.change_pct <= -0.03:
        market_signal = "DOWN"
    else:
        market_signal = "STABLE"

    return SetIntelligence(
        set_id=set_id,
        available_conditions=conditions,
        fair_prices=fair_prices,
        strongest_change=strongest_change,
        market_signal=market_signal,
        summary=_build_set_summary(set_id, fair_prices, strongest_change, market_signal),
    )


def _confidence_for_snapshot_count(snapshot_count: int) -> Confidence:
    if snapshot_count >= 5:
        return "HIGH"
    if snapshot_count >= 3:
        return "MEDIUM"
    if snapshot_count >= 1:
        return "LOW"
    return "NONE"


def _build_set_summary(
    set_id: str,
    fair_prices: list[FairPrice],
    strongest_change: PriceChange | None,
    market_signal: str,
) -> str:
    if not fair_prices:
        return f"No hay histórico seed suficiente para construir inteligencia de mercado del set {set_id}."

    best_price = max(
        fair_prices,
        key=lambda price: price.avg_eur if price.avg_eur is not None else -1,
    )

    if strongest_change is None:
        return (
            f"El set {set_id} tiene precio dinámico disponible, pero todavía no acumula "
            "suficientes puntos temporales para medir tendencia."
        )

    direction = "subiendo" if strongest_change.change_pct > 0 else "bajando"
    return (
        f"El set {set_id} muestra señal {market_signal}. La condición {best_price.condition} "
        f"tiene fair price estimado de {best_price.avg_eur} EUR y el mercado reciente está "
        f"{direction} un {round(strongest_change.change_pct * 100, 2)}%."
    )
