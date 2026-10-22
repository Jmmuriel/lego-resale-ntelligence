"""The V1 Streamlit app honours LRI_DEMO_ALLOW_WRITES like the V2 API."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.db import ListingAnalysisRecord
from src.placeholders import mock_analyze_listing


APP_PATH = str(Path(__file__).resolve().parents[1] / "app" / "main.py")
LISTING_URL = "https://www.ebay.es/itm/lego-75192"


def _fail(*args, **kwargs):
    raise AssertionError("the read-only Streamlit app must not write to the database")


@pytest.fixture
def stub_data_layer(monkeypatch):
    record = ListingAnalysisRecord(id=7, status="watching", url=LISTING_URL, set_id="75192", risk_flags=[])
    monkeypatch.setattr("src.db.list_recent_listings", lambda limit=20: [record])
    monkeypatch.setattr("src.pipeline.analyze_listing_url", mock_analyze_listing)


def _run_app() -> AppTest:
    return AppTest.from_file(APP_PATH, default_timeout=30).run()


def _button(app: AppTest, label: str):
    return next(button for button in app.button if button.label == label)


def test_streamlit_analyzes_without_saving_by_default(monkeypatch, stub_data_layer):
    monkeypatch.setattr("src.db.save_listing_analysis", _fail)
    monkeypatch.setattr("src.db.update_listing_status", _fail)
    app = _run_app()

    labels = [button.label for button in app.button]
    assert "Analyze and save" not in labels
    assert "Update status" not in labels

    app.text_input[0].input(LISTING_URL)
    _button(app, "Analyze").click().run()

    assert not app.exception
    assert "solo lectura" in "".join(block.value for block in app.markdown)


def test_streamlit_saves_when_writes_are_enabled(monkeypatch, stub_data_layer, allow_demo_writes):
    saved = []

    def fake_save(analysis):
        saved.append(analysis)
        return ListingAnalysisRecord(id=8, status="analyzed", url=analysis.url, risk_flags=[])

    monkeypatch.setattr("src.db.save_listing_analysis", fake_save)
    app = _run_app()

    assert "Update status" in [button.label for button in app.button]

    app.text_input[0].input(LISTING_URL)
    _button(app, "Analyze and save").click().run()

    assert not app.exception
    assert [analysis.url for analysis in saved] == [LISTING_URL]
