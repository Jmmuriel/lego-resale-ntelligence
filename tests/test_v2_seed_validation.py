import json
from pathlib import Path

from scripts.v2_validate_seed_data import validate_seed_data


def test_current_v2_seed_data_is_valid():
    report = validate_seed_data(target_catalog_size=10)

    assert report["ok"] is True
    assert report["errors"] == []
    assert report["metrics"]["catalog_sets"] == 10
    assert report["metrics"]["catalog_candidate_sets"] == 40
    assert report["metrics"]["catalog_plus_candidates"] == 50
    assert report["metrics"]["price_snapshots"] == 50
    assert report["metrics"]["portfolio_items"] == 3


def test_validation_reports_catalog_below_guide_target():
    report = validate_seed_data()

    assert report["ok"] is True
    assert any(
        warning["code"] == "CATALOG_BELOW_TARGET"
        for warning in report["warnings"]
    )


def test_validation_catches_unknown_price_history_set(tmp_path):
    catalog_path = _write_catalog(tmp_path)
    price_history_path = tmp_path / "price_history_seed.json"
    portfolio_path = tmp_path / "portfolio_seed.json"
    price_history_path.write_text(
        json.dumps(
            [
                {
                    "set_id": "00000",
                    "condition": "USED_COMPLETE",
                    "source": "manual",
                    "price_min_eur": 10.0,
                    "price_avg_eur": 12.0,
                    "price_max_eur": 15.0,
                    "sample_count": 3,
                    "recorded_at": "2026-05-14",
                }
            ]
        ),
        encoding="utf-8",
    )
    portfolio_path.write_text("[]", encoding="utf-8")

    report = validate_seed_data(
        catalog_path=catalog_path,
        price_history_path=price_history_path,
        portfolio_path=portfolio_path,
        candidates_path=None,
        target_catalog_size=1,
    )

    assert report["ok"] is False
    assert report["errors"][0]["code"] == "PRICE_UNKNOWN_SET"


def test_validation_catches_invalid_price_band(tmp_path):
    catalog_path = _write_catalog(tmp_path)
    price_history_path = tmp_path / "price_history_seed.json"
    portfolio_path = tmp_path / "portfolio_seed.json"
    price_history_path.write_text(
        json.dumps(
            [
                {
                    "set_id": "75192",
                    "condition": "USED_COMPLETE",
                    "source": "manual",
                    "price_min_eur": 20.0,
                    "price_avg_eur": 12.0,
                    "price_max_eur": 15.0,
                    "sample_count": 3,
                    "recorded_at": "2026-05-14",
                }
            ]
        ),
        encoding="utf-8",
    )
    portfolio_path.write_text("[]", encoding="utf-8")

    report = validate_seed_data(
        catalog_path=catalog_path,
        price_history_path=price_history_path,
        portfolio_path=portfolio_path,
        candidates_path=None,
        target_catalog_size=1,
    )

    assert report["ok"] is False
    assert report["errors"][0]["code"] == "PRICE_BAND_INVALID"


def _write_catalog(tmp_path: Path) -> Path:
    catalog_path = tmp_path / "catalog.csv"
    catalog_path.write_text(
        "\n".join(
            [
                "set_id,name,theme,year_released,year_retired,retail_price_eur,pieces,popularity_score",
                "75192,Millennium Falcon,Star Wars,2017,2024,849.99,7541,10",
            ]
        ),
        encoding="utf-8",
    )
    return catalog_path
