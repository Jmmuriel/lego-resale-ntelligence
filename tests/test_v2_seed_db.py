from sqlalchemy import select

from backend.db.database import get_session_factory
from backend.db.models import PortfolioItem, PriceHistory, SetCatalog
from scripts.v2_seed_db import seed_database

EXPECTED_CATALOG_SETS = 50
EXPECTED_PRICE_HISTORY = 250


def test_seed_database_loads_catalog_price_history_and_portfolio(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'lri_v2.db'}"

    counts = seed_database(database_url)

    assert counts["catalog_sets"] == EXPECTED_CATALOG_SETS
    assert counts["price_history"] == EXPECTED_PRICE_HISTORY
    assert counts["portfolio_items"] == 3

    session_factory = get_session_factory(database_url)
    with session_factory() as session:
        catalog_count = len(session.scalars(select(SetCatalog)).all())
        price_count = len(session.scalars(select(PriceHistory)).all())
        portfolio_count = len(session.scalars(select(PortfolioItem)).all())

    assert catalog_count == EXPECTED_CATALOG_SETS
    assert price_count == EXPECTED_PRICE_HISTORY
    assert portfolio_count == 3


def test_seed_database_is_idempotent(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'lri_v2.db'}"

    seed_database(database_url)
    seed_database(database_url)

    session_factory = get_session_factory(database_url)
    with session_factory() as session:
        catalog_count = len(session.scalars(select(SetCatalog)).all())
        price_count = len(session.scalars(select(PriceHistory)).all())
        portfolio_count = len(session.scalars(select(PortfolioItem)).all())

    assert catalog_count == EXPECTED_CATALOG_SETS
    assert price_count == EXPECTED_PRICE_HISTORY
    assert portfolio_count == 3
