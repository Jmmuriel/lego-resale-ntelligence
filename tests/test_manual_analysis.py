from src.manual_analysis import analyze_manual_listing
from src.models import ListingInput


def test_analyze_manual_listing_with_known_reference():
    listing_input = ListingInput(
        url="https://www.ebay.es/itm/lego-75192",
        marketplace="ebay",
        asking_price_eur=560.0,
        shipping_eur=25.0,
    )

    analysis = analyze_manual_listing(
        listing_input=listing_input,
        set_id="75192",
        condition="USED_COMPLETE",
    )

    assert analysis.fair_price_eur == 720.0
    assert analysis.gross_margin_eur is not None
    assert analysis.net_margin_eur is not None


def test_analyze_manual_listing_without_reference():
    listing_input = ListingInput(
        url="https://example.com/listing/lego",
        marketplace="unknown",
        asking_price_eur=100.0,
        shipping_eur=5.0,
    )

    analysis = analyze_manual_listing(
        listing_input=listing_input,
        set_id="00000",
        condition="UNKNOWN",
    )

    assert analysis.fair_price_eur is None
    assert "Sin referencia manual de fair price" in analysis.risk_flags
    assert analysis.notes is not None


def test_manual_analysis_score_is_between_zero_and_one_hundred():
    listing_input = ListingInput(
        url="https://es.wallapop.com/item/lego-10221",
        marketplace="wallapop",
        asking_price_eur=340.0,
        shipping_eur=12.0,
    )

    analysis = analyze_manual_listing(
        listing_input=listing_input,
        set_id="10221",
        condition="UNKNOWN",
    )

    assert analysis.opportunity_score is not None
    assert 0 <= analysis.opportunity_score <= 100


def test_manual_analysis_category_is_valid():
    listing_input = ListingInput(
        url="https://www.vinted.es/items/lego-21309",
        marketplace="vinted",
        asking_price_eur=82.0,
        shipping_eur=8.0,
    )

    analysis = analyze_manual_listing(
        listing_input=listing_input,
        set_id="21309",
        condition="USED_COMPLETE",
    )

    assert analysis.category in {"GREEN", "YELLOW", "RED"}


def test_manual_analysis_margins_are_present_with_reference():
    listing_input = ListingInput(
        url="https://www.ebay.es/itm/lego-75192",
        marketplace="ebay",
        asking_price_eur=560.0,
        shipping_eur=25.0,
    )

    analysis = analyze_manual_listing(
        listing_input=listing_input,
        set_id="75192",
        condition="USED_COMPLETE",
    )

    assert analysis.gross_margin_eur is not None
    assert analysis.net_margin_eur is not None
