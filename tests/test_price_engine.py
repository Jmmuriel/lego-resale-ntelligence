from datetime import date

from backend.services.price_engine import (
    PriceSnapshot,
    compute_anomaly_score,
    compute_fair_price,
    exponential_decay_weights,
    get_price_changes,
    get_set_intelligence,
    load_price_snapshots,
    load_price_snapshots_from_db,
    load_price_snapshots_from_json,
    market_reference_date,
)
from scripts.v2_seed_db import seed_database


AS_OF = date(2026, 5, 14)


def test_exponential_decay_weights_sum_to_one():
    weights = exponential_decay_weights(
        [date(2026, 3, 14), date(2026, 4, 14), date(2026, 5, 14)],
        as_of=AS_OF,
    )

    assert round(sum(weights), 6) == 1
    assert weights[-1] > weights[0]


def test_compute_fair_price_with_complete_history_has_high_confidence():
    fair_price = compute_fair_price(
        "75192",
        "USED_COMPLETE",
        as_of=AS_OF,
    )

    assert fair_price.set_id == "75192"
    assert fair_price.confidence == "HIGH"
    assert fair_price.snapshot_count == 5
    assert fair_price.sample_count == 97  # 16 + 18 + 20 + 22 + 21 in the seed history
    assert fair_price.avg_eur is not None
    assert 720.0 < fair_price.avg_eur < 742.0
    assert fair_price.days_since_update == 0


def test_compute_fair_price_with_sparse_history_has_low_confidence():
    snapshots = [
        PriceSnapshot(
            set_id="10214",
            condition="SEALED",
            source="manual",
            price_min_eur=260.0,
            price_avg_eur=280.0,
            price_max_eur=325.0,
            sample_count=9,
            recorded_at=AS_OF,
        )
    ]

    fair_price = compute_fair_price(
        "10214",
        "SEALED",
        as_of=AS_OF,
        snapshots=snapshots,
    )

    assert fair_price.confidence == "LOW"
    assert fair_price.avg_eur == 280.0


def test_compute_fair_price_without_history_returns_none_confidence():
    fair_price = compute_fair_price(
        "00000",
        "USED_COMPLETE",
        as_of=AS_OF,
        snapshots=[],
    )

    assert fair_price.confidence == "NONE"
    assert fair_price.avg_eur is None


def test_compute_anomaly_score_marks_discount_as_negative():
    anomaly_score = compute_anomaly_score(
        asking_price_eur=560.0,
        fair_avg_eur=700.0,
    )

    assert anomaly_score == -0.2


def test_compute_anomaly_score_marks_expensive_listing_as_positive():
    anomaly_score = compute_anomaly_score(
        asking_price_eur=840.0,
        fair_avg_eur=700.0,
    )

    assert anomaly_score == 0.2


def test_get_price_changes_orders_by_strongest_movement():
    changes = get_price_changes(days=90, as_of=AS_OF)

    assert changes
    assert changes[0].set_id == "75192"
    assert changes[0].change_pct > 0


def test_get_set_intelligence_returns_summary_for_known_set():
    intelligence = get_set_intelligence("75192", days=120, as_of=AS_OF)

    assert intelligence.set_id == "75192"
    assert intelligence.available_conditions == ["USED_COMPLETE"]
    assert intelligence.fair_prices[0].confidence == "HIGH"
    assert intelligence.strongest_change is not None
    assert intelligence.market_signal == "UP"
    assert "75192" in intelligence.summary


def test_get_set_intelligence_handles_unknown_set():
    intelligence = get_set_intelligence("00000", days=120, as_of=AS_OF, snapshots=[])

    assert intelligence.available_conditions == []
    assert intelligence.fair_prices == []
    assert intelligence.strongest_change is None
    assert intelligence.market_signal == "UNKNOWN"


def test_load_price_snapshots_from_db_reads_seeded_database(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'v2.db'}"
    seed_database(database_url)

    snapshots = load_price_snapshots_from_db(database_url)

    assert len(snapshots) == len(load_price_snapshots_from_json())
    assert any(snapshot.set_id == "75192" for snapshot in snapshots)


def test_load_price_snapshots_prefers_db_when_available(monkeypatch):
    db_snapshot = PriceSnapshot(
        set_id="DB_ONLY",
        condition="SEALED",
        source="db",
        price_min_eur=10.0,
        price_avg_eur=12.0,
        price_max_eur=15.0,
        sample_count=2,
        recorded_at=AS_OF,
    )

    monkeypatch.setattr(
        "backend.services.price_engine.load_price_snapshots_from_db",
        lambda: [db_snapshot],
    )

    assert load_price_snapshots() == [db_snapshot]


def _snapshot(recorded_at: date) -> PriceSnapshot:
    return PriceSnapshot(
        set_id="75192",
        condition="USED_COMPLETE",
        source="test",
        price_min_eur=600.0,
        price_avg_eur=700.0,
        price_max_eur=800.0,
        sample_count=10,
        recorded_at=recorded_at,
    )


def test_market_reference_date_follows_stale_demo_history(monkeypatch):
    monkeypatch.delenv("LRI_MARKET_REFERENCE_DATE", raising=False)
    snapshots = [_snapshot(date(2026, 4, 14)), _snapshot(date(2026, 5, 14))]

    assert market_reference_date(snapshots, today=date(2026, 10, 15)) == date(2026, 5, 15)


def test_market_reference_date_is_today_with_live_data(monkeypatch):
    monkeypatch.delenv("LRI_MARKET_REFERENCE_DATE", raising=False)
    snapshots = [_snapshot(date(2026, 10, 15))]

    assert market_reference_date(snapshots, today=date(2026, 10, 15)) == date(2026, 10, 15)


def test_market_reference_date_can_be_pinned(monkeypatch):
    monkeypatch.setenv("LRI_MARKET_REFERENCE_DATE", "2026-03-01")

    assert market_reference_date([_snapshot(date(2026, 5, 14))], today=date(2026, 10, 15)) == date(2026, 3, 1)


def test_default_windows_keep_demo_trends_after_the_seed_period(monkeypatch):
    monkeypatch.delenv("LRI_MARKET_REFERENCE_DATE", raising=False)
    seed = load_price_snapshots_from_json()

    assert get_price_changes(snapshots=seed)
    assert compute_fair_price("75192", "USED_COMPLETE", snapshots=seed).confidence == "HIGH"
