from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.db.models import PortfolioItem, PriceHistory, SetCatalog, Transaction


def upsert_set_catalog(session: Session, set_item: SetCatalog) -> SetCatalog:
    """Insert or update a catalog set by `set_id`."""
    existing = session.get(SetCatalog, set_item.set_id)
    if existing is None:
        session.add(set_item)
        session.flush()
        return set_item

    for field in [
        "name",
        "theme",
        "year_released",
        "year_retired",
        "retail_price_eur",
        "pieces",
        "popularity_score",
        "metadata_json",
    ]:
        setattr(existing, field, getattr(set_item, field))

    session.flush()
    return existing


def list_catalog_sets(session: Session, limit: int = 50) -> list[SetCatalog]:
    """Return catalog sets ordered by set id."""
    statement = select(SetCatalog).order_by(SetCatalog.set_id).limit(limit)
    return list(session.scalars(statement).all())


def replace_price_history(session: Session, snapshots: list[PriceHistory]) -> int:
    """Replace seeded price history with a deterministic source of truth."""
    session.execute(delete(PriceHistory))
    session.add_all(snapshots)
    session.flush()
    return len(snapshots)


def replace_portfolio_items(session: Session, items: list[PortfolioItem]) -> int:
    """Replace demo portfolio items with deterministic seed data."""
    session.execute(delete(Transaction))
    session.execute(delete(PortfolioItem))
    session.add_all(items)
    session.flush()
    return len(items)
