import pytest

from src.models import ListingAnalysis, ListingExtraction, ListingInput
from src.placeholders import mock_analyze_listing


def test_listing_input_can_be_created():
    listing = ListingInput(
        url="https://www.ebay.es/itm/example",
        marketplace="ebay",
        asking_price_eur=620.0,
        shipping_eur=18.0,
    )

    assert listing.url == "https://www.ebay.es/itm/example"
    assert listing.marketplace == "ebay"
    assert listing.asking_price_eur == 620.0


def test_listing_extraction_can_be_created():
    extraction = ListingExtraction(
        set_id="75192",
        title_clean="LEGO Star Wars Millennium Falcon",
        condition="USED_COMPLETE",
        description_summary="Set usado aparentemente completo.",
        risk_flags=["Confirmar minifiguras"],
    )

    assert extraction.set_id == "75192"
    assert extraction.risk_flags == ["Confirmar minifiguras"]


def test_listing_analysis_can_be_created():
    analysis = ListingAnalysis(
        url="https://www.wallapop.com/item/example",
        marketplace="wallapop",
        set_id="10221",
        condition="UNKNOWN",
        asking_price_eur=340.0,
        shipping_eur=12.0,
        fair_price_eur=430.0,
        gross_margin_eur=42.0,
        net_margin_eur=18.0,
        opportunity_score=61,
        category="YELLOW",
        risk_flags=["Negociar precio"],
        notes="Caso viable con cautela.",
    )

    assert analysis.category == "YELLOW"
    assert analysis.opportunity_score == 61


@pytest.mark.parametrize(
    ("url", "expected_marketplace"),
    [
        ("https://www.ebay.es/itm/lego-75192", "ebay"),
        ("https://es.wallapop.com/item/lego-10221", "wallapop"),
        ("https://www.vinted.es/items/lego-21309", "vinted"),
        ("https://example.com/listing/lego", "unknown"),
    ],
)
def test_mock_analyze_listing_detects_marketplace(url, expected_marketplace):
    analysis = mock_analyze_listing(url)

    assert analysis.marketplace == expected_marketplace
    assert isinstance(analysis, ListingAnalysis)
