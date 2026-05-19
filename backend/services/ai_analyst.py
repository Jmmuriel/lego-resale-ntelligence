import logging
import os
from datetime import date, datetime, timedelta, timezone
from typing import Literal

from pydantic import BaseModel

from backend.services.portfolio_engine import PortfolioSummary, get_portfolio_summary
from backend.services.price_engine import PriceChange, get_price_changes

log = logging.getLogger(__name__)


MarketTrend = Literal["BULLISH", "NEUTRAL", "BEARISH"]

BRIEFING_SYSTEM_PROMPT = """
Eres el analista ejecutivo de LEGO Resale Intelligence.
Genera briefings breves, concretos y accionables sobre mercado de LEGO retirado.
No inventes datos. Si una sección no tiene datos suficientes, dilo claramente.
Estructura fija:
1. Resumen ejecutivo
2. Movimientos de mercado
3. Portfolio
4. Acción recomendada
Tono: ejecutivo, directo, en español, máximo 350 palabras.
""".strip()


class MarketBriefing(BaseModel):
    """Generated market briefing for the V2 intelligence layer."""

    period_start: date
    period_end: date
    briefing_text: str
    key_opportunities: list[str]
    market_trend: MarketTrend
    generated_at: datetime
    model_version: str
    token_count: int
    used_llm: bool = False


def _build_briefing_context(
    market_trend: "MarketTrend",
    price_changes: list["PriceChange"],
    portfolio_summary: "PortfolioSummary",
    period_days: int,
) -> str:
    """Serialize current V2 data into a structured prompt context block."""
    top_moves = _format_price_moves(price_changes)
    return (
        f"PERIOD: last {period_days} days\n"
        f"MARKET_TREND: {market_trend}\n"
        f"OPEN_POSITIONS: {portfolio_summary.open_positions}\n"
        f"UNREALIZED_PNL_EUR: {portfolio_summary.total_unrealized_pnl_eur:.2f}\n"
        f"UNREALIZED_PNL_PCT: {portfolio_summary.total_unrealized_pnl_pct:.2f}\n"
        f"DOMINANT_SIGNAL: {portfolio_summary.dominant_signal}\n"
        f"PRICE_MOVEMENTS:\n{top_moves}"
    )


def generate_briefing_with_llm(period_days: int = 7) -> MarketBriefing:
    """Generate a briefing using Claude Sonnet with local deterministic fallback.

    Falls back silently to the deterministic version if the API key is missing,
    Anthropic is unreachable, or any other error occurs — so the app never breaks.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        log.info("ANTHROPIC_API_KEY not set — using local deterministic briefing")
        return generate_briefing(period_days=period_days)

    try:
        import anthropic  # noqa: PLC0415

        now = datetime.now(timezone.utc)
        period_end = now.date()
        period_start = period_end - timedelta(days=period_days)
        price_changes = get_price_changes(days=max(period_days, 120))[:5]
        portfolio_summary = get_portfolio_summary()
        market_trend = infer_market_trend(price_changes)
        context = _build_briefing_context(market_trend, price_changes, portfolio_summary, period_days)

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=BRIEFING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": context}],
        )
        briefing_text = response.content[0].text
        token_count = response.usage.input_tokens + response.usage.output_tokens
        key_opportunities = _key_opportunities(price_changes, portfolio_summary)

        return MarketBriefing(
            period_start=period_start,
            period_end=period_end,
            briefing_text=briefing_text,
            key_opportunities=key_opportunities,
            market_trend=market_trend,
            generated_at=now,
            model_version="claude-sonnet-4-6",
            token_count=token_count,
            used_llm=True,
        )
    except Exception as exc:
        log.warning("LLM briefing failed (%s) — falling back to local deterministic", exc)
        return generate_briefing(period_days=period_days)


def generate_briefing(period_days: int = 7) -> MarketBriefing:
    """Generate a deterministic briefing from current V2 seed data."""
    now = datetime.now(timezone.utc)
    period_end = now.date()
    period_start = period_end - timedelta(days=period_days)
    price_changes = get_price_changes(days=max(period_days, 120))[:3]
    portfolio_summary = get_portfolio_summary()
    market_trend = infer_market_trend(price_changes)
    key_opportunities = _key_opportunities(price_changes, portfolio_summary)
    briefing_text = _compose_briefing_text(
        market_trend=market_trend,
        price_changes=price_changes,
        portfolio_summary=portfolio_summary,
        period_days=period_days,
    )

    return MarketBriefing(
        period_start=period_start,
        period_end=period_end,
        briefing_text=briefing_text,
        key_opportunities=key_opportunities,
        market_trend=market_trend,
        generated_at=now,
        model_version="local-deterministic-v0",
        token_count=0,
        used_llm=False,
    )


def get_latest_briefings(limit: int = 1) -> list[MarketBriefing]:
    """Return generated briefing history.

    Until persistence exists, this returns a fresh deterministic briefing.
    """
    return [generate_briefing() for _ in range(limit)]


def infer_market_trend(price_changes: list[PriceChange]) -> MarketTrend:
    """Infer coarse market tone from recent price movements."""
    if not price_changes:
        return "NEUTRAL"

    average_change = sum(change.change_pct for change in price_changes) / len(price_changes)
    if average_change >= 0.03:
        return "BULLISH"
    if average_change <= -0.03:
        return "BEARISH"
    return "NEUTRAL"


def _compose_briefing_text(
    market_trend: MarketTrend,
    price_changes: list[PriceChange],
    portfolio_summary: PortfolioSummary,
    period_days: int,
) -> str:
    top_moves = _format_price_moves(price_changes)
    pnl_direction = "positivo" if portfolio_summary.total_unrealized_pnl_eur >= 0 else "negativo"
    action = _recommended_action(market_trend, portfolio_summary)

    return (
        f"## Resumen ejecutivo\n"
        f"Mercado {market_trend} en los últimos {period_days} días según el histórico seed disponible. "
        f"El portfolio tiene P&L no realizado {pnl_direction} de "
        f"{portfolio_summary.total_unrealized_pnl_eur:.2f} EUR "
        f"({portfolio_summary.total_unrealized_pnl_pct:.2f}%).\n\n"
        f"## Movimientos de mercado\n"
        f"{top_moves}\n\n"
        f"## Portfolio\n"
        f"{portfolio_summary.open_positions} posiciones abiertas. Señal dominante: "
        f"{portfolio_summary.dominant_signal}. Mejor posición ID: "
        f"{portfolio_summary.top_position_id}; peor posición ID: "
        f"{portfolio_summary.worst_position_id}.\n\n"
        f"## Acción recomendada\n"
        f"{action}"
    )


def _format_price_moves(price_changes: list[PriceChange]) -> str:
    if not price_changes:
        return "Datos insuficientes para detectar movimientos relevantes."

    lines = []
    for change in price_changes[:3]:
        direction = "sube" if change.change_pct >= 0 else "baja"
        lines.append(
            f"- Set {change.set_id} ({change.condition}) {direction} "
            f"{change.change_pct * 100:.2f}%: "
            f"{change.start_avg_eur:.2f} EUR -> {change.end_avg_eur:.2f} EUR."
        )
    return "\n".join(lines)


def _recommended_action(
    market_trend: MarketTrend,
    portfolio_summary: PortfolioSummary,
) -> str:
    if portfolio_summary.dominant_signal == "SELL":
        return "Revisar las posiciones marcadas como SELL antes de buscar nuevas compras."
    if market_trend == "BULLISH":
        return "Priorizar seguimiento de oportunidades con anomaly score negativo y confianza alta."
    if market_trend == "BEARISH":
        return "Ser más selectivo: exigir mayor margen neto y evitar compras con precio poco confiable."
    return "Mantener watchlist activa y esperar señales más fuertes antes de aumentar exposición."


def _key_opportunities(
    price_changes: list[PriceChange],
    portfolio_summary: PortfolioSummary,
) -> list[str]:
    set_ids = [change.set_id for change in price_changes[:3]]
    if portfolio_summary.top_position_id is not None:
        set_ids.append(f"portfolio_position_{portfolio_summary.top_position_id}")
    return set_ids
