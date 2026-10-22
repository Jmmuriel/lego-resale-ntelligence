import pytest

from src.extract import build_extraction_prompt, call_anthropic, parse_extraction_response
from src.limits import LLMBudgetExceeded
from src.models import ListingExtraction


def test_build_extraction_prompt_includes_listing_text():
    prompt = build_extraction_prompt(
        "LEGO Star Wars 75192 Millennium Falcon usado completo con caja."
    )

    assert "75192" in prompt
    assert "USED_COMPLETE" in prompt
    assert "JSON válido" in prompt


def test_build_extraction_prompt_truncates_long_listing_text(monkeypatch):
    monkeypatch.setenv("LRI_LLM_MAX_INPUT_CHARS", "50")

    prompt = build_extraction_prompt("LEGO 75192 " + "a" * 10_000 + " FINAL_MARKER")

    assert "LEGO 75192" in prompt
    assert "FINAL_MARKER" not in prompt
    assert "a" * 51 not in prompt


def test_build_extraction_prompt_caps_input_at_4000_chars_by_default():
    prompt = build_extraction_prompt("b" * 10_000)

    assert "b" * 4000 in prompt
    assert "b" * 4001 not in prompt


def test_call_anthropic_respects_daily_cap_before_calling_api(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("LRI_LLM_DAILY_CAP", "0")

    def fail_client(*args, **kwargs):
        raise AssertionError("the Anthropic client must not be created over the daily cap")

    monkeypatch.setattr("anthropic.Anthropic", fail_client)

    with pytest.raises(LLMBudgetExceeded):
        call_anthropic("prompt")


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
