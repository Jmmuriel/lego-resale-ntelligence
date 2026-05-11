from src.capture import fetch_html, parse_listing_html
from src.db import DATABASE_URL, ListingAnalysisRecord, save_listing_analysis
from src.extract import extract_listing
from src.identify import identify_set
from src.models import ListingAnalysis, ListingExtraction, ListingInput
from src.pricing_reference import get_fair_price
from src.scoring import (
    categorize_score,
    compute_gross_margin,
    compute_net_margin,
    compute_opportunity_score,
)


class PipelineError(RuntimeError):
    """Error controlado del flujo end-to-end de Fase 2."""


def analyze_listing_url(url: str) -> ListingAnalysis:
    """Ejecuta el flujo mínimo: captura, extracción, identificación, pricing y scoring."""
    if not url or not url.strip():
        raise PipelineError("La URL no puede estar vacía.")

    html = fetch_html(url)
    listing_input = parse_listing_html(html, url=url)
    raw_text = _build_raw_text(listing_input)
    if not raw_text:
        raise PipelineError("El HTML no contiene título ni descripción útiles para analizar.")

    extraction = _safe_extract_listing(raw_text)
    catalog_set = identify_set(
        set_id=extraction.set_id,
        title=extraction.title_clean,
    )
    if catalog_set is None:
        raise PipelineError("No se pudo identificar el set contra el catálogo local.")

    fair_price_eur = get_fair_price(
        set_id=catalog_set.set_id,
        condition=extraction.condition,
    )
    if fair_price_eur is None:
        raise PipelineError("No hay fair price manual disponible para el set identificado.")

    if listing_input.asking_price_eur is None:
        raise PipelineError("No se pudo extraer el precio pedido del listing.")

    return _build_listing_analysis(
        url=url,
        listing_input=listing_input,
        extraction=extraction,
        set_id=catalog_set.set_id,
        fair_price_eur=fair_price_eur,
    )


def analyze_and_save_listing_url(
    url: str,
    database_url: str = DATABASE_URL,
) -> ListingAnalysisRecord:
    """Analiza una URL y guarda el resultado en SQLite."""
    analysis = analyze_listing_url(url)
    return save_listing_analysis(analysis, database_url=database_url)


def _build_raw_text(listing_input: ListingInput) -> str:
    """Une título y descripción en texto crudo para el extractor LLM."""
    parts = [
        listing_input.raw_title,
        listing_input.raw_description,
    ]

    return "\n".join(part for part in parts if part).strip()


def _safe_extract_listing(raw_text: str) -> ListingExtraction:
    """Envuelve errores del extractor para que el pipeline falle con un mensaje claro."""
    try:
        return extract_listing(raw_text)
    except Exception as exc:
        raise PipelineError(f"La extracción estructurada falló: {exc}") from exc


def _build_listing_analysis(
    url: str,
    listing_input: ListingInput,
    extraction: ListingExtraction,
    set_id: str,
    fair_price_eur: float,
) -> ListingAnalysis:
    """Construye el análisis final a partir de los datos ya identificados."""
    asking_price_eur = listing_input.asking_price_eur
    shipping_eur = listing_input.shipping_eur
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
    net_margin_pct = (net_margin_eur / acquisition_cost) * 100 if acquisition_cost > 0 else 0.0
    opportunity_score = compute_opportunity_score(
        net_margin_pct=net_margin_pct,
        risk_flags=extraction.risk_flags,
        marketplace=listing_input.marketplace,
    )
    category = categorize_score(
        score=opportunity_score,
        net_margin_eur=net_margin_eur,
    )

    return ListingAnalysis(
        url=url,
        marketplace=listing_input.marketplace,
        set_id=set_id,
        condition=extraction.condition,
        asking_price_eur=asking_price_eur,
        shipping_eur=shipping_eur,
        fair_price_eur=fair_price_eur,
        gross_margin_eur=gross_margin_eur,
        net_margin_eur=net_margin_eur,
        opportunity_score=opportunity_score,
        category=category,
        risk_flags=extraction.risk_flags,
        notes=f"Flujo end-to-end Fase 2. {extraction.description_summary}",
    )
