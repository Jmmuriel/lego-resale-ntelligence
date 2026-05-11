from src.scoring import (
    build_margin_breakdown,
    compute_gross_margin,
    compute_net_margin,
    compute_opportunity_score,
    categorize_score,
    normalize_margin_score,
)


def test_build_margin_breakdown():
    breakdown = build_margin_breakdown(
        asking_price_eur=100.0,
        shipping_eur=10.0,
        fair_price_eur=150.0,
    )

    assert breakdown["asking_price_eur"] == 100.0
    assert breakdown["shipping_eur"] == 10.0
    assert breakdown["acquisition_cost"] == 110.0
    assert breakdown["fair_price_eur"] == 150.0
    assert breakdown["selling_fees"] == 15.0
    assert breakdown["shipping_out"] == 8.0
    assert breakdown["net_revenue"] == 127.0
    assert breakdown["net_margin_eur"] == 17.0


def test_compute_gross_margin():
    result = compute_gross_margin(
        asking_price_eur=100.0,
        shipping_eur=10.0,
        fair_price_eur=150.0,
    )

    assert result == 40.0


def test_compute_net_margin():
    result = compute_net_margin(
        asking_price_eur=100.0,
        shipping_eur=10.0,
        fair_price_eur=150.0,
    )

    assert result == 17.0


def test_normalize_margin_score():
    assert normalize_margin_score(-5.0) == 0
    assert normalize_margin_score(0.0) == 0
    assert normalize_margin_score(20.0) == 50
    assert normalize_margin_score(40.0) == 100
    assert normalize_margin_score(80.0) == 100


def test_categorize_score():
    assert categorize_score(score=75, net_margin_eur=30.0) == "GREEN"
    assert categorize_score(score=55, net_margin_eur=10.0) == "YELLOW"
    assert categorize_score(score=30, net_margin_eur=50.0) == "RED"
    assert categorize_score(score=80, net_margin_eur=5.0) == "RED"


def test_high_opportunity_becomes_green():
    score = compute_opportunity_score(
        net_margin_pct=45.0,
        risk_flags=[],
        marketplace="ebay",
    )

    assert score == 100
    assert categorize_score(score, net_margin_eur=80.0) == "GREEN"


def test_medium_opportunity_becomes_yellow():
    score = compute_opportunity_score(
        net_margin_pct=25.0,
        risk_flags=["Confirmar piezas"],
        marketplace=None,
    )

    assert score == 54
    assert categorize_score(score, net_margin_eur=18.0) == "YELLOW"


def test_bad_opportunity_becomes_red():
    score = compute_opportunity_score(
        net_margin_pct=-3.0,
        risk_flags=["Margen insuficiente", "Faltan piezas"],
        marketplace="vinted",
    )

    assert score == 0
    assert categorize_score(score, net_margin_eur=-12.0) == "RED"
