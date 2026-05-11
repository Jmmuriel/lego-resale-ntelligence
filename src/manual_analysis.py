from src.models import ListingAnalysis, ListingInput
from src.pricing_reference import get_fair_price
from src.scoring import (
    compute_gross_margin,
    compute_net_margin,
    compute_opportunity_score,
    categorize_score,
)


def analyze_manual_listing(
    listing_input: ListingInput,
    set_id: str | None,
    condition: str,
) -> ListingAnalysis:
    """Analiza un listing introducido manualmente por el usuario."""
    clean_set_id = set_id.strip() if set_id else None
    analysis_url = listing_input.url or "manual-input"
    risk_flags: list[str] = []
    fair_price_eur = get_fair_price(clean_set_id, condition)

    if fair_price_eur is None:
        return ListingAnalysis(
            url=analysis_url,
            marketplace=listing_input.marketplace,
            set_id=clean_set_id,
            condition=condition,
            asking_price_eur=listing_input.asking_price_eur,
            shipping_eur=listing_input.shipping_eur,
            risk_flags=["Sin referencia manual de fair price"],
            notes="No hay una referencia manual para este set y condición. Añádela antes de confiar en el análisis.",
        )

    if listing_input.asking_price_eur is None:
        return ListingAnalysis(
            url=analysis_url,
            marketplace=listing_input.marketplace,
            set_id=clean_set_id,
            condition=condition,
            fair_price_eur=fair_price_eur,
            shipping_eur=listing_input.shipping_eur,
            risk_flags=["Falta precio de compra"],
            notes="No se puede calcular el margen porque falta el precio pedido por el vendedor.",
        )

    gross_margin_eur = compute_gross_margin(
        asking_price_eur=listing_input.asking_price_eur,
        shipping_eur=listing_input.shipping_eur,
        fair_price_eur=fair_price_eur,
    )
    net_margin_eur = compute_net_margin(
        asking_price_eur=listing_input.asking_price_eur,
        shipping_eur=listing_input.shipping_eur,
        fair_price_eur=fair_price_eur,
    )

    acquisition_cost = listing_input.asking_price_eur + (listing_input.shipping_eur or 0.0)
    net_margin_pct = (net_margin_eur / acquisition_cost) * 100 if acquisition_cost > 0 else 0
    opportunity_score = compute_opportunity_score(
        net_margin_pct=net_margin_pct,
        risk_flags=risk_flags,
        marketplace=listing_input.marketplace,
    )
    category = categorize_score(
        score=opportunity_score,
        net_margin_eur=net_margin_eur,
    )

    return ListingAnalysis(
        url=analysis_url,
        marketplace=listing_input.marketplace,
        set_id=clean_set_id,
        condition=condition,
        asking_price_eur=listing_input.asking_price_eur,
        shipping_eur=listing_input.shipping_eur,
        fair_price_eur=fair_price_eur,
        gross_margin_eur=gross_margin_eur,
        net_margin_eur=net_margin_eur,
        opportunity_score=opportunity_score,
        category=category,
        risk_flags=risk_flags,
        notes="Análisis manual calculado con referencia interna de fair price.",
    )
