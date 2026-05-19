from datetime import date

from backend.services.portfolio_engine import (
    PortfolioItem,
    compute_hold_sell_signal,
    compute_position_pnl,
    get_portfolio_summary,
    load_portfolio_items,
    load_portfolio_items_from_db,
    load_portfolio_items_from_json,
)
from scripts.v2_seed_db import seed_database


AS_OF = date(2026, 5, 14)


def test_compute_position_pnl_uses_dynamic_fair_price():
    item = PortfolioItem(
        id=1,
        set_id="75192",
        set_name="Millennium Falcon (UCS)",
        condition="USED_COMPLETE",
        quantity=1,
        cost_basis_eur=585.0,
        purchased_at=date(2026, 2, 10),
        status="HOLDING",
    )

    pnl = compute_position_pnl(item, as_of=AS_OF)

    assert pnl.price_confidence == "HIGH"
    assert pnl.current_fair_value_eur > 700
    assert pnl.unrealized_pnl_eur > 0
    assert pnl.days_held == 93


def test_compute_position_pnl_without_price_history_is_neutral():
    item = PortfolioItem(
        id=99,
        set_id="00000",
        set_name="Unknown Set",
        condition="USED_COMPLETE",
        quantity=1,
        cost_basis_eur=100.0,
        purchased_at=date(2026, 5, 1),
        status="HOLDING",
    )

    pnl = compute_position_pnl(item, as_of=AS_OF)

    assert pnl.price_confidence == "NONE"
    assert pnl.current_fair_value_eur == 100.0
    assert pnl.hold_sell_signal == "NEUTRAL"


def test_compute_hold_sell_signal_sells_strong_profit_after_holding():
    signal, reason = compute_hold_sell_signal(
        unrealized_pnl_pct=32.0,
        trend_direction="UP",
        days_held=120,
        price_confidence="HIGH",
    )

    assert signal == "SELL"
    assert "beneficio" in reason


def test_portfolio_summary_rolls_up_positions():
    items = [
        PortfolioItem(
            id=1,
            set_id="75192",
            set_name="Millennium Falcon (UCS)",
            condition="USED_COMPLETE",
            quantity=1,
            cost_basis_eur=585.0,
            purchased_at=date(2026, 2, 10),
            status="HOLDING",
        ),
        PortfolioItem(
            id=2,
            set_id="75313",
            set_name="AT-AT (UCS)",
            condition="USED_COMPLETE",
            quantity=1,
            cost_basis_eur=690.0,
            purchased_at=date(2026, 3, 3),
            status="HOLDING",
        ),
    ]

    summary = get_portfolio_summary(as_of=AS_OF, items=items)

    assert summary.open_positions == 2
    assert summary.total_cost_basis_eur == 1275.0
    assert summary.total_current_fair_value_eur > summary.total_cost_basis_eur
    assert summary.top_position_id in {1, 2}


def test_load_portfolio_items_from_db_reads_seeded_database(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'v2.db'}"
    seed_database(database_url)

    items = load_portfolio_items_from_db(database_url)

    assert len(items) == len(load_portfolio_items_from_json())
    assert items[0].set_id == "75192"
    assert items[0].id is not None


def test_load_portfolio_items_prefers_db_when_available(monkeypatch):
    db_item = PortfolioItem(
        id=99,
        set_id="DB_ONLY",
        set_name="DB Only Set",
        condition="SEALED",
        quantity=1,
        cost_basis_eur=10.0,
        purchased_at=AS_OF,
        status="HOLDING",
    )

    monkeypatch.setattr(
        "backend.services.portfolio_engine.load_portfolio_items_from_db",
        lambda: [db_item],
    )

    assert load_portfolio_items() == [db_item]
