from src.capture import detect_marketplace_from_url, parse_listing_html
from src.models import ListingInput


def test_parse_listing_html_extracts_title():
    html = """
    <html>
      <body>
        <h1>LEGO Star Wars 75192 Millennium Falcon</h1>
        <p class="price">650,00 €</p>
      </body>
    </html>
    """

    listing = parse_listing_html(html, url="https://www.ebay.es/itm/lego-75192")

    assert listing.raw_title == "LEGO Star Wars 75192 Millennium Falcon"


def test_parse_listing_html_extracts_description_if_present():
    html = """
    <html>
      <body>
        <h1>LEGO Ideas 21309 NASA Apollo Saturn V</h1>
        <div class="description">Set usado completo con instrucciones.</div>
      </body>
    </html>
    """

    listing = parse_listing_html(html, url="https://es.wallapop.com/item/lego-21309")

    assert listing.raw_description == "Set usado completo con instrucciones."


def test_detect_marketplace_from_url():
    assert detect_marketplace_from_url("https://www.ebay.es/itm/123") == "ebay"
    assert detect_marketplace_from_url("https://es.wallapop.com/item/123") == "wallapop"
    assert detect_marketplace_from_url("https://www.vinted.es/items/123") == "vinted"
    assert detect_marketplace_from_url("https://example.com/item/123") == "unknown"
    assert detect_marketplace_from_url(None) is None


def test_parse_listing_html_does_not_break_with_missing_fields():
    listing = parse_listing_html("<html><body></body></html>")

    assert isinstance(listing, ListingInput)
    assert listing.url is None
    assert listing.raw_title is None
    assert listing.raw_description is None
    assert listing.asking_price_eur is None
    assert listing.shipping_eur is None


def test_parse_listing_html_returns_listing_input_with_prices():
    html = """
    <html>
      <body>
        <h1>LEGO Imperial Star Destroyer 10221</h1>
        <span class="price">399.99 €</span>
        <span>Envío 12,50 €</span>
      </body>
    </html>
    """

    listing = parse_listing_html(html, url="https://www.ebay.es/itm/lego-10221")

    assert isinstance(listing, ListingInput)
    assert listing.marketplace == "ebay"
    assert listing.asking_price_eur == 399.99
    assert listing.shipping_eur == 12.5


def test_parse_listing_html_prefers_meta_title_over_generic_heading():
    html = """
    <html>
      <head>
        <meta property="og:title" content="LEGO Star Wars 75192 Millennium Falcon" />
      </head>
      <body>
        <h1>Todas las categorías</h1>
        <span class="price">799,95 €</span>
      </body>
    </html>
    """

    listing = parse_listing_html(html, url="https://es.wallapop.com/item/lego-75192")

    assert listing.raw_title == "LEGO Star Wars 75192 Millennium Falcon"
    assert listing.asking_price_eur == 799.95


def test_parse_listing_html_reads_basic_json_ld_product_data():
    html = """
    <html>
      <head>
        <script type="application/ld+json">
          {
            "@type": "Product",
            "name": "LEGO Ideas 21309 NASA Apollo Saturn V",
            "description": "Set usado completo con caja.",
            "offers": {
              "price": "145.00"
            }
          }
        </script>
      </head>
      <body></body>
    </html>
    """

    listing = parse_listing_html(html, url="https://es.wallapop.com/item/lego-21309")

    assert listing.raw_title == "LEGO Ideas 21309 NASA Apollo Saturn V"
    assert listing.raw_description == "Set usado completo con caja."
    assert listing.asking_price_eur == 145.0


def test_parse_listing_html_does_not_confuse_price_after_shipping_text():
    html = """
    <html>
      <body>
        <h1>LEGO Star Wars 75095 TIE Fighter UCS</h1>
        <p>Entrega en mano o envío parcialmente desmontado y protegido.</p>
        <p class="price">350 €</p>
      </body>
    </html>
    """

    listing = parse_listing_html(html, url="https://es.wallapop.com/item/lego-75095")

    assert listing.asking_price_eur == 350.0
    assert listing.shipping_eur is None
