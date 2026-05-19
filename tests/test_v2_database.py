from datetime import date

from backend.db.database import Base, get_session_factory, init_v2_db
from backend.db.crud import list_catalog_sets, upsert_set_catalog
from backend.db.models import SetCatalog


def test_v2_metadata_contains_guide_tables():
    expected_tables = {
        "set_catalog",
        "price_history",
        "listings",
        "portfolio_items",
        "transactions",
        "market_briefings",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_v2_init_db_creates_tables(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'lri_v2.db'}"
    engine = init_v2_db(database_url)

    assert set(Base.metadata.tables).issubset(engine.dialect.get_table_names(engine.connect()))


def test_v2_catalog_upsert_round_trip(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'lri_v2.db'}"
    init_v2_db(database_url)
    session_factory = get_session_factory(database_url)

    with session_factory() as session:
        upsert_set_catalog(
            session,
            SetCatalog(
                set_id="75192",
                name="Millennium Falcon",
                theme="Star Wars",
                year_released=2017,
                year_retired=2024,
                retail_price_eur=849.99,
                pieces=7541,
                popularity_score=10,
                metadata_json={"source": "test"},
            ),
        )
        session.commit()

    with session_factory() as session:
        sets = list_catalog_sets(session)

    assert len(sets) == 1
    assert sets[0].set_id == "75192"
    assert sets[0].metadata_json == {"source": "test"}
