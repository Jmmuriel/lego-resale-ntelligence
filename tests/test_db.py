import pytest

from src.db import (
    ListingAnalysisRecord,
    init_db,
    list_recent_listings,
    save_listing_analysis,
    update_listing_status,
)
from src.models import ListingAnalysis


def test_init_db_creates_sqlite_file(tmp_path):
    database_path = tmp_path / "test_lri.db"
    database_url = f"sqlite:///{database_path}"

    init_db(database_url)

    assert database_path.exists()


def test_save_listing_analysis_persists_record(tmp_path):
    database_url = _temp_database_url(tmp_path)
    analysis = _sample_analysis()

    record = save_listing_analysis(analysis, database_url=database_url)

    assert isinstance(record, ListingAnalysisRecord)
    assert record.id is not None
    assert record.url == analysis.url
    assert record.risk_flags == ["Confirmar piezas completas"]


def test_list_recent_listings_returns_saved_records(tmp_path):
    database_url = _temp_database_url(tmp_path)
    save_listing_analysis(_sample_analysis(url="https://example.com/one"), database_url)
    save_listing_analysis(_sample_analysis(url="https://example.com/two"), database_url)

    records = list_recent_listings(limit=1, database_url=database_url)

    assert len(records) == 1
    assert records[0].url == "https://example.com/two"


def test_update_listing_status_changes_status(tmp_path):
    database_url = _temp_database_url(tmp_path)
    record = save_listing_analysis(_sample_analysis(), database_url=database_url)

    updated = update_listing_status(record.id, "watching", database_url=database_url)

    assert updated is not None
    assert updated.status == "watching"


def test_update_listing_status_returns_none_for_missing_record(tmp_path):
    database_url = _temp_database_url(tmp_path)

    updated = update_listing_status(999, "discarded", database_url=database_url)

    assert updated is None


def test_update_listing_status_rejects_invalid_status(tmp_path):
    database_url = _temp_database_url(tmp_path)
    record = save_listing_analysis(_sample_analysis(), database_url=database_url)

    with pytest.raises(ValueError, match="Estado inválido"):
        update_listing_status(record.id, "invalid", database_url=database_url)


def _temp_database_url(tmp_path) -> str:
    return f"sqlite:///{tmp_path / 'test_lri.db'}"


def _sample_analysis(url: str = "https://www.ebay.es/itm/lego-75192") -> ListingAnalysis:
    return ListingAnalysis(
        url=url,
        marketplace="ebay",
        set_id="75192",
        condition="USED_COMPLETE",
        asking_price_eur=560.0,
        shipping_eur=25.0,
        fair_price_eur=720.0,
        gross_margin_eur=135.0,
        net_margin_eur=55.0,
        opportunity_score=72,
        category="GREEN",
        risk_flags=["Confirmar piezas completas"],
        notes="Análisis de prueba.",
    )
