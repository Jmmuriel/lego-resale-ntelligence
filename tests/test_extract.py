import pytest

from src.extract import build_extraction_prompt, parse_extraction_response
from src.models import ListingExtraction


def test_build_extraction_prompt_includes_listing_text():
    prompt = build_extraction_prompt(
        "LEGO Star Wars 75192 Millennium Falcon usado completo con caja."
    )

    assert "75192" in prompt
    assert "USED_COMPLETE" in prompt
    assert "JSON válido" in prompt


def test_build_extraction_prompt_rejects_empty_input():
    with pytest.raises(ValueError, match="no puede estar vacío"):
        build_extraction_prompt("   ")


def test_parse_extraction_response_returns_listing_extraction():
    response_text = """
    {
      "set_id": "75192",
      "title_clean": "LEGO Star Wars Millennium Falcon",
      "condition": "USED_COMPLETE",
      "description_summary": "Set usado completo con caja e instrucciones.",
      "risk_flags": []
    }
    """

    extraction = parse_extraction_response(response_text)

    assert isinstance(extraction, ListingExtraction)
    assert extraction.set_id == "75192"
    assert extraction.condition == "USED_COMPLETE"


def test_parse_extraction_response_accepts_markdown_json_block():
    response_text = """
    ```json
    {
      "set_id": "75192",
      "title_clean": "LEGO Star Wars Millennium Falcon",
      "condition": "USED_COMPLETE",
      "description_summary": "Set usado completo con caja e instrucciones.",
      "risk_flags": []
    }
    ```
    """

    extraction = parse_extraction_response(response_text)

    assert extraction.set_id == "75192"
    assert extraction.condition == "USED_COMPLETE"


def test_parse_extraction_response_rejects_empty_response():
    with pytest.raises(ValueError, match="está vacía"):
        parse_extraction_response("")


def test_parse_extraction_response_rejects_invalid_json():
    with pytest.raises(ValueError, match="no es JSON válido"):
        parse_extraction_response("no soy json")


def test_parse_extraction_response_rejects_invalid_schema():
    response_text = """
    {
      "set_id": "75192",
      "title_clean": "LEGO Star Wars Millennium Falcon",
      "condition": "BROKEN",
      "description_summary": "Set usado completo.",
      "risk_flags": []
    }
    """

    with pytest.raises(ValueError, match="schema esperado"):
        parse_extraction_response(response_text)
