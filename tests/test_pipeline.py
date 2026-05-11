import pytest

from src.models import ListingExtraction
from src.pipeline import PipelineError, analyze_and_save_listing_url, analyze_listing_url


def test_analyze_listing_url_runs_end_to_end_with_mocks(monkeypatch):
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: _sample_html())
    monkeypatch.setattr("src.pipeline.extract_listing", lambda raw_text: _sample_extraction())

    analysis = analyze_listing_url("https://www.ebay.es/itm/lego-75192")

    assert analysis.url == "https://www.ebay.es/itm/lego-75192"
    assert analysis.marketplace == "ebay"
    assert analysis.set_id == "75192"
    assert analysis.condition == "USED_COMPLETE"
    assert analysis.fair_price_eur == 720.0
    assert analysis.gross_margin_eur is not None
    assert analysis.net_margin_eur is not None
    assert 0 <= analysis.opportunity_score <= 100


def test_analyze_and_save_listing_url_persists_result(monkeypatch, tmp_path):
    database_url = f"sqlite:///{tmp_path / 'pipeline.db'}"
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: _sample_html())
    monkeypatch.setattr("src.pipeline.extract_listing", lambda raw_text: _sample_extraction())

    record = analyze_and_save_listing_url(
        "https://www.ebay.es/itm/lego-75192",
        database_url=database_url,
    )

    assert record.id is not None
    assert record.set_id == "75192"
    assert record.status == "analyzed"


def test_analyze_listing_url_rejects_empty_url():
    with pytest.raises(PipelineError, match="URL no puede estar vacía"):
        analyze_listing_url("  ")


def test_analyze_listing_url_rejects_html_without_useful_data(monkeypatch):
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: "<html><body></body></html>")

    with pytest.raises(PipelineError, match="HTML no contiene"):
        analyze_listing_url("https://www.ebay.es/itm/empty")


def test_analyze_listing_url_wraps_extraction_errors(monkeypatch):
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: _sample_html())

    def fail_extraction(raw_text):
        raise ValueError("respuesta inválida")

    monkeypatch.setattr("src.pipeline.extract_listing", fail_extraction)

    with pytest.raises(PipelineError, match="extracción estructurada falló"):
        analyze_listing_url("https://www.ebay.es/itm/lego-75192")


def test_analyze_listing_url_rejects_unidentified_set(monkeypatch):
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: _sample_html())
    monkeypatch.setattr(
        "src.pipeline.extract_listing",
        lambda raw_text: ListingExtraction(
            set_id=None,
            title_clean="LEGO desconocido",
            condition="UNKNOWN",
            description_summary="Listing sin set identificable.",
            risk_flags=[],
        ),
    )

    with pytest.raises(PipelineError, match="No se pudo identificar"):
        analyze_listing_url("https://www.ebay.es/itm/unknown")


def test_analyze_listing_url_rejects_missing_fair_price(monkeypatch):
    monkeypatch.setattr("src.pipeline.fetch_html", lambda url: _sample_html())
    monkeypatch.setattr("src.pipeline.get_fair_price", lambda set_id, condition: None)
    monkeypatch.setattr(
        "src.pipeline.extract_listing",
        lambda raw_text: ListingExtraction(
            set_id="75192",
            title_clean="LEGO Star Wars Millennium Falcon",
            condition="USED_COMPLETE",
            description_summary="Set usado completo.",
            risk_flags=[],
        ),
    )

    with pytest.raises(PipelineError, match="fair price"):
        analyze_listing_url("https://www.ebay.es/itm/lego-75192")


def _sample_html() -> str:
    return """
    <html>
      <body>
        <h1>LEGO Star Wars 75192 Millennium Falcon</h1>
        <div class="description">Set usado completo con caja e instrucciones.</div>
        <span class="price">560,00 €</span>
        <span>Envío 25,00 €</span>
      </body>
    </html>
    """


def _sample_extraction() -> ListingExtraction:
    return ListingExtraction(
        set_id="75192",
        title_clean="LEGO Star Wars Millennium Falcon",
        condition="USED_COMPLETE",
        description_summary="Set usado completo con caja e instrucciones.",
        risk_flags=["Confirmar piezas completas"],
    )
