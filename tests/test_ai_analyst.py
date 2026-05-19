from backend.services.ai_analyst import (
    BRIEFING_SYSTEM_PROMPT,
    generate_briefing,
    infer_market_trend,
)
from backend.services.price_engine import PriceChange


def test_briefing_system_prompt_sets_clear_structure():
    assert "Resumen ejecutivo" in BRIEFING_SYSTEM_PROMPT
    assert "No inventes datos" in BRIEFING_SYSTEM_PROMPT
    assert "350 palabras" in BRIEFING_SYSTEM_PROMPT


def test_infer_market_trend_detects_bullish_market():
    trend = infer_market_trend(
        [
            PriceChange(
                set_id="75192",
                condition="USED_COMPLETE",
                start_avg_eur=690.0,
                end_avg_eur=742.0,
                change_eur=52.0,
                change_pct=0.0754,
            )
        ]
    )

    assert trend == "BULLISH"


def test_generate_briefing_uses_local_data_without_llm_cost():
    briefing = generate_briefing(period_days=7)

    assert briefing.used_llm is False
    assert briefing.token_count == 0
    assert briefing.model_version == "local-deterministic-v0"
    assert briefing.market_trend in {"BULLISH", "NEUTRAL", "BEARISH"}
    assert "Resumen ejecutivo" in briefing.briefing_text
    assert "Portfolio" in briefing.briefing_text
    assert briefing.key_opportunities
