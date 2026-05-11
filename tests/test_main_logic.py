from src.placeholders import mock_analyze_listing


def test_placeholder_analysis_returns_coherent_result():
    analysis = mock_analyze_listing("https://www.ebay.es/itm/lego-75192")

    assert analysis.url == "https://www.ebay.es/itm/lego-75192"
    assert analysis.marketplace == "ebay"
    assert analysis.set_id is not None
    assert analysis.condition is not None
    assert analysis.asking_price_eur is not None
    assert analysis.shipping_eur is not None
    assert analysis.fair_price_eur is not None
    assert analysis.gross_margin_eur is not None
    assert analysis.net_margin_eur is not None
    assert analysis.gross_margin_eur >= analysis.net_margin_eur
    assert 0 <= analysis.opportunity_score <= 100
    assert analysis.category in {"GREEN", "YELLOW", "RED"}
    assert analysis.notes
