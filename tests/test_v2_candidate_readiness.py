import json

from backend.services.data_quality import list_catalog_candidates
from scripts.v2_check_candidate_readiness import check_candidate_readiness


def test_candidate_readiness_blocks_candidates_without_evidence(tmp_path):
    candidates_csv = tmp_path / "catalog_expansion_candidates.csv"
    candidates_csv.write_text(
        "set_id,name,theme,reason,validation_status\n"
        "99999,Test Set,Star Wars,Test candidate,needs_research\n",
        encoding="utf-8",
    )

    from backend.services import data_quality as dq
    original = dq.CATALOG_CANDIDATES_PATH
    dq.CATALOG_CANDIDATES_PATH = candidates_csv
    try:
        candidates = list_catalog_candidates()
    finally:
        dq.CATALOG_CANDIDATES_PATH = original

    first_candidate = candidates[0]

    assert first_candidate.readiness.ready_for_promotion is False
    assert first_candidate.readiness.completed_checks == 0
    assert "release year" in first_candidate.readiness.missing_requirements
    assert "3 price snapshots" in first_candidate.readiness.missing_requirements


def test_candidate_readiness_accepts_complete_evidence(tmp_path):
    candidates_csv = tmp_path / "catalog_expansion_candidates.csv"
    candidates_csv.write_text(
        "set_id,name,theme,reason,validation_status\n"
        "10212,Imperial Shuttle,Star Wars,UCS candidate,needs_research\n",
        encoding="utf-8",
    )
    research_path = tmp_path / "catalog_candidate_research.json"
    research_path.write_text(
        json.dumps(
            {
                "version": 1,
                "candidates": [
                    {
                        "set_id": "10212",
                        "year_released": 2010,
                        "year_retired": 2012,
                        "retail_price_eur": 259.99,
                        "pieces": 2503,
                        "popularity_score": 9,
                        "metadata_sources": [
                            "https://example.com/metadata-a",
                            "https://example.com/metadata-b",
                        ],
                        "price_sources": [
                            "https://example.com/prices-a",
                            "https://example.com/prices-b",
                        ],
                        "price_snapshots": [
                            {"price_avg_eur": 500},
                            {"price_avg_eur": 520},
                            {"price_avg_eur": 540},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    from backend.services import data_quality as dq
    original = dq.CATALOG_CANDIDATES_PATH
    dq.CATALOG_CANDIDATES_PATH = candidates_csv
    try:
        candidates = list_catalog_candidates(research_path=research_path)
    finally:
        dq.CATALOG_CANDIDATES_PATH = original
    target = next(candidate for candidate in candidates if candidate.set_id == "10212")

    assert target.readiness.ready_for_promotion is True
    assert target.readiness.completed_checks == target.readiness.required_checks


def test_candidate_readiness_cli_returns_not_found_code():
    assert check_candidate_readiness("10212") == 1
