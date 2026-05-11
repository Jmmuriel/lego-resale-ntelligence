from src.models import ListingAnalysis
from src.pricing_reference import get_fair_price
from src.scoring import (
    compute_gross_margin,
    compute_net_margin,
    compute_opportunity_score,
    categorize_score,
)


def detect_marketplace(url: str) -> str:
    """Detecta el marketplace de forma básica a partir de la URL."""
    url_lower = url.lower()

    if "ebay" in url_lower:
        return "ebay"
    if "wallapop" in url_lower:
        return "wallapop"
    if "vinted" in url_lower:
        return "vinted"

    return "unknown"


def mock_analyze_listing(url: str) -> ListingAnalysis:
    """Genera un análisis simulado y determinista para arrancar la Fase 2."""
    marketplace = detect_marketplace(url)

    examples = {
        "ebay": {
            "set_id": "75192",
            "condition": "USED_COMPLETE",
            "asking_price_eur": 560.0,
            "shipping_eur": 25.0,
            "risk_flags": ["Confirmar piezas completas", "Revisar coste real de envío"],
            "notes": "Oportunidad interesante si el estado es bueno y el envío no reduce demasiado el margen.",
        },
        "wallapop": {
            "set_id": "10221",
            "condition": "UNKNOWN",
            "asking_price_eur": 340.0,
            "shipping_eur": 12.0,
            "risk_flags": ["Confirmar caja e instrucciones", "Negociar precio antes de comprar"],
            "notes": "Puede ser viable, pero necesita validación manual y algo de negociación.",
        },
        "vinted": {
            "set_id": "21309",
            "condition": "USED_COMPLETE",
            "asking_price_eur": 82.0,
            "shipping_eur": 8.0,
            "risk_flags": ["Margen insuficiente", "Verificar que no falten piezas"],
            "notes": "No parece una prioridad para compra en esta fase.",
        },
        "unknown": {
            "set_id": "10221",
            "condition": "UNKNOWN",
            "asking_price_eur": 345.0,
            "shipping_eur": None,
            "risk_flags": ["Marketplace no reconocido", "Validar precio manualmente"],
            "notes": "Análisis conservador porque el marketplace no se reconoce automáticamente.",
        },
    }

    example = examples[marketplace]
    set_id = example["set_id"]
    condition = example["condition"]
    asking_price_eur = example["asking_price_eur"]
    shipping_eur = example["shipping_eur"]
    risk_flags = example["risk_flags"]
    fair_price_eur = get_fair_price(set_id=set_id, condition=condition)

    if fair_price_eur is None:
        return ListingAnalysis(
            url=url,
            marketplace=marketplace,
            set_id=set_id,
            condition=condition,
            asking_price_eur=asking_price_eur,
            shipping_eur=shipping_eur,
            risk_flags=[*risk_flags, "Sin referencia manual de fair price"],
            notes="No se pudo calcular el análisis porque falta una referencia manual de precio.",
        )

    gross_margin_eur = compute_gross_margin(
        asking_price_eur=asking_price_eur,
        shipping_eur=shipping_eur,
        fair_price_eur=fair_price_eur,
    )
    net_margin_eur = compute_net_margin(
        asking_price_eur=asking_price_eur,
        shipping_eur=shipping_eur,
        fair_price_eur=fair_price_eur,
    )

    acquisition_cost = asking_price_eur + (shipping_eur or 0.0)
    net_margin_pct = (net_margin_eur / acquisition_cost) * 100
    opportunity_score = compute_opportunity_score(
        net_margin_pct=net_margin_pct,
        risk_flags=risk_flags,
        marketplace=marketplace,
    )
    category = categorize_score(
        score=opportunity_score,
        net_margin_eur=net_margin_eur,
    )

    return ListingAnalysis(
        url=url,
        marketplace=marketplace,
        set_id=set_id,
        condition=condition,
        asking_price_eur=asking_price_eur,
        shipping_eur=shipping_eur,
        fair_price_eur=fair_price_eur,
        gross_margin_eur=gross_margin_eur,
        net_margin_eur=net_margin_eur,
        opportunity_score=opportunity_score,
        category=category,
        risk_flags=risk_flags,
        notes=example["notes"],
    )
