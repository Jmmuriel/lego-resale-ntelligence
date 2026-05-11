FEES_RATE = 0.10
SHIPPING_OUT = 8.0
MAX_MARGIN_PCT_FOR_FULL_SCORE = 40.0


def build_margin_breakdown(
    asking_price_eur: float | None,
    shipping_eur: float | None,
    fair_price_eur: float | None,
) -> dict[str, float | None]:
    """Construye un desglose simple del cálculo del margen neto."""
    shipping_in = shipping_eur or 0.0
    acquisition_cost = None
    selling_fees = None
    net_revenue = None
    net_margin_eur = None

    if asking_price_eur is not None:
        acquisition_cost = round(asking_price_eur + shipping_in, 2)

    if fair_price_eur is not None:
        selling_fees = round(fair_price_eur * FEES_RATE, 2)
        net_revenue = round(fair_price_eur - selling_fees - SHIPPING_OUT, 2)

    if acquisition_cost is not None and net_revenue is not None:
        net_margin_eur = round(net_revenue - acquisition_cost, 2)

    return {
        "asking_price_eur": asking_price_eur,
        "shipping_eur": shipping_in,
        "acquisition_cost": acquisition_cost,
        "fair_price_eur": fair_price_eur,
        "selling_fees": selling_fees,
        "shipping_out": SHIPPING_OUT,
        "net_revenue": net_revenue,
        "net_margin_eur": net_margin_eur,
    }


def compute_gross_margin(
    asking_price_eur: float,
    shipping_eur: float | None,
    fair_price_eur: float,
) -> float:
    """Calcula el margen bruto antes de comisiones y envío de salida."""
    shipping_in = shipping_eur or 0.0
    acquisition_cost = asking_price_eur + shipping_in

    return round(fair_price_eur - acquisition_cost, 2)


def compute_net_margin(
    asking_price_eur: float,
    shipping_eur: float | None,
    fair_price_eur: float,
) -> float:
    """Calcula el margen neto estimado después de costes principales."""
    shipping_in = shipping_eur or 0.0
    acquisition_cost = asking_price_eur + shipping_in
    selling_fees = fair_price_eur * FEES_RATE
    net_revenue = fair_price_eur - selling_fees - SHIPPING_OUT

    return round(net_revenue - acquisition_cost, 2)


def normalize_margin_score(net_margin_pct: float) -> int:
    """Convierte un margen porcentual en una puntuación entre 0 y 100."""
    if net_margin_pct <= 0:
        return 0

    if net_margin_pct >= MAX_MARGIN_PCT_FOR_FULL_SCORE:
        return 100

    score = (net_margin_pct / MAX_MARGIN_PCT_FOR_FULL_SCORE) * 100
    return round(score)


def compute_opportunity_score(
    net_margin_pct: float,
    risk_flags: list[str],
    marketplace: str | None = None,
) -> int:
    """Calcula un score simple combinando margen, riesgos y marketplace."""
    margin_score = normalize_margin_score(net_margin_pct)
    risk_penalty = len(risk_flags) * 8
    marketplace_bonus = 0

    if marketplace in {"ebay", "wallapop"}:
        marketplace_bonus = 5

    score = margin_score - risk_penalty + marketplace_bonus
    return max(0, min(100, score))


def categorize_score(score: int, net_margin_eur: float) -> str:
    """Clasifica la oportunidad en una categoría fácil de interpretar."""
    if score >= 70 and net_margin_eur > 20:
        return "GREEN"

    if 45 <= score <= 69:
        return "YELLOW"

    return "RED"
