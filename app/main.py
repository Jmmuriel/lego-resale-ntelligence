import base64
from html import escape
from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
LEGO_LOGO_PATH = APP_DIR / "assets" / "lego_logo.png"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from styles import apply_global_styles
from src.db import ListingAnalysisRecord, list_recent_listings, save_listing_analysis
from src.models import ListingAnalysis
from src.pipeline import PipelineError, analyze_listing_url
from src.scoring import build_margin_breakdown


PHASE_LABEL = "Phase 3B Premium Streamlit Experience"


def format_eur(value: float | None) -> str:
    """Formatea importes en euros para mostrarlos en pantalla."""
    if value is None:
        return "N/D"
    return f"{value:.2f} EUR"


def format_condition(value: str | None) -> str:
    """Hace más legibles las condiciones técnicas en la interfaz."""
    if value is None:
        return "N/D"
    return value.replace("_", " ")


def safe_text(value: object) -> str:
    """Escapa texto antes de renderizarlo dentro de HTML propio."""
    if value is None:
        return "N/D"
    return escape(str(value))


def image_data_uri(path: Path) -> str:
    """Convierte una imagen local en data URI para usarla dentro del HTML."""
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def metric_card(label: str, value: object) -> str:
    """Devuelve una card de métrica en HTML (compact — sin newlines para evitar code blocks en Markdown)."""
    return (
        f'<div class="lri-metric">'
        f'<div class="lri-metric-label">{safe_text(label)}</div>'
        f'<div class="lri-metric-value">{safe_text(value)}</div>'
        f'</div>'
    )


def status_panel(title: str, message: str, tone: str = "neutral") -> None:
    """Muestra estados premium para empty, error, loading o success."""
    st.markdown(
        f"""
        <div class="lri-status-panel {safe_text(tone)}">
            <div class="lri-status-dot"></div>
            <div>
                <div class="lri-status-title">{safe_text(title)}</div>
                <div class="lri-status-message">{safe_text(message)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pipeline_error_feedback(error: Exception) -> tuple[str, str, str]:
    """Traduce errores técnicos del pipeline a mensajes claros de producto."""
    error_text = str(error)
    normalized = error_text.lower()

    if "no se pudo descargar el html" in normalized:
        return (
            "Listing capture failed",
            "El marketplace no ha permitido descargar el HTML o el listing ya no está disponible.",
            "Prueba otra URL activa. En eBay esto puede pasar por bloqueos 403; en Wallapop suele pasar con listings borrados o 404.",
        )

    if "no contiene título ni descripción" in normalized:
        return (
            "No useful listing text found",
            "La página se descargó, pero el HTML no traía título o descripción suficientes para analizar.",
            "Prueba con una URL de listing más completa o revisa si el marketplace está ocultando el contenido.",
        )

    if "extracción estructurada falló" in normalized:
        return (
            "Anthropic extraction failed",
            "La captura llegó al paso LLM, pero Anthropic no pudo devolver una extracción válida.",
            "Revisa la API key, créditos disponibles y que el texto del listing sea suficientemente claro.",
        )

    if "no se pudo identificar el set" in normalized:
        return (
            "Set not found in local catalog",
            "El sistema no pudo cruzar el listing contra `data/catalog.csv` con suficiente confianza.",
            "Para que funcione, el set debe aparecer claramente en el título o estar cubierto por el catálogo local.",
        )

    if "fair price manual" in normalized:
        return (
            "No fair price reference",
            "El set se identificó, pero todavía no hay referencia manual de fair price para esa condición.",
            "Añade ese set y condición a `src/pricing_reference.py` antes de usarlo para scoring real.",
        )

    if "precio pedido" in normalized:
        return (
            "Asking price not detected",
            "El sistema no pudo leer un precio pedido claro desde el HTML del listing.",
            "Prueba otra URL o usa este caso para mejorar el parser de precios más adelante.",
        )

    return (
        "Controlled pipeline stop",
        error_text,
        "El flujo se detuvo de forma controlada para evitar guardar un análisis poco fiable.",
    )


def show_error_panel(error: Exception) -> None:
    """Muestra errores reales con título, causa y siguiente acción."""
    title, message, next_step = pipeline_error_feedback(error)
    status_panel(title, f"{message} Siguiente paso: {next_step}", tone="error")


def show_topline() -> None:
    """Muestra la marca superior común."""
    lego_logo_uri = image_data_uri(LEGO_LOGO_PATH)
    st.markdown(
        f"""
        <div class="lri-topline">
            <div class="lri-mark">
                <img class="lri-mark-logo" src="{lego_logo_uri}" alt="LEGO logo" />
                <span>LEGO Resale Intelligence</span>
            </div>
            <div>{PHASE_LABEL}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_navigation() -> str:
    """Renderiza navegación simple entre secciones de Fase 3A."""
    overview_tab, analyze_tab, about_tab = st.tabs(["Overview", "Analyze", "About"])
    return overview_tab, analyze_tab, about_tab


def show_overview() -> None:
    """Landing editorial premium de la app."""
    lego_logo_uri = image_data_uri(LEGO_LOGO_PATH)
    st.markdown(
        f"""
        <section class="lri-hero">
            <div class="lri-hero-copy">
                <div class="lri-kicker">Collector-grade resale intelligence</div>
                <h1 class="lri-title">A calmer way to read retired LEGO opportunity.</h1>
                <p class="lri-subtitle">
                    LEGO Resale Intelligence turns marketplace noise into a focused buying signal:
                    fair price, net margin, risk flags and an opportunity score for retired sets.
                </p>
                <div class="lri-hero-actions">
                    <span class="lri-cta">Use the Analyze tab</span>
                    <span class="lri-ghost-cta">Phase 3B polished</span>
                </div>
            </div>
            <div class="lri-object-stage" aria-hidden="true">
                <div class="lri-logo-plinth">
                    <img class="lri-lego-logo" src="{lego_logo_uri}" alt="LEGO logo" />
                </div>
            </div>
        </section>
        <div class="lri-stat-grid">
            <div class="lri-stat">
                <div class="lri-stat-value">20+</div>
                <div class="lri-stat-label">real listings tested</div>
            </div>
            <div class="lri-stat">
                <div class="lri-stat-value">64</div>
                <div class="lri-stat-label">automated tests passing</div>
            </div>
            <div class="lri-stat">
                <div class="lri-stat-value">10</div>
                <div class="lri-stat-label">catalog sets covered</div>
            </div>
            <div class="lri-stat">
                <div class="lri-stat-value">1</div>
                <div class="lri-stat-label">local SQLite archive</div>
            </div>
        </div>
        <div class="lri-editorial-grid">
            <div class="lri-editorial-card">
                <div class="lri-card-index">01 / Signal</div>
                <div class="lri-card-title">Price discipline over impulse browsing.</div>
                <div class="lri-card-copy">
                    The app translates asking price, fair price and resale costs into a single
                    opportunity reading.
                </div>
            </div>
            <div class="lri-editorial-card">
                <div class="lri-card-index">02 / Collection</div>
                <div class="lri-card-title">A museum-like surface for retired sets.</div>
                <div class="lri-card-copy">
                    The visual system treats listings as collectible objects, not generic rows
                    in a spreadsheet.
                </div>
            </div>
            <div class="lri-editorial-card">
                <div class="lri-card-index">03 / Intelligence</div>
                <div class="lri-card-title">LLM extraction, local scoring, clear limits.</div>
                <div class="lri-card-copy">
                    Anthropic structures listing text; the Python core keeps scoring explicit,
                    testable and easy to explain.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_input_panel() -> str:
    """Renderiza el panel principal de entrada."""
    st.markdown(
        """
        <div class="lri-input-intro">
            <div class="lri-section-label">
                <span>Listing intake</span>
                <span>URL analysis</span>
            </div>
            <div class="lri-input-copy">
                Paste one listing URL. The system will keep the current flow local, explicit and traceable.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    listing_url = st.text_input(
        "URL del listing",
        placeholder="https://es.wallapop.com/item/...",
        label_visibility="collapsed",
    )

    return listing_url


def show_analyze() -> None:
    """Pantalla operativa de análisis."""
    st.markdown(
        """
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Analyze</span>
                <span>live pipeline</span>
            </div>
            <div class="lri-manifesto">
                Paste a listing URL. The system captures the HTML, extracts structured data,
                identifies the LEGO set, calculates margin and stores the result locally.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    listing_url = show_input_panel()

    if st.button("Analyze and save"):
        if not listing_url:
            status_panel(
                "URL required",
                "Introduce una URL real de listing antes de lanzar el análisis.",
                tone="warning",
            )
        else:
            try:
                loading_placeholder = st.empty()
                with loading_placeholder.container():
                    status_panel(
                        "Reading the market signal",
                        "Capturando HTML, extrayendo datos con Anthropic y calculando oportunidad.",
                        tone="loading",
                    )
                with st.spinner(""):
                    analysis = analyze_listing_url(listing_url)
                    record = save_listing_analysis(analysis)
                loading_placeholder.empty()
            except PipelineError as exc:
                show_error_panel(exc)
            except Exception as exc:
                status_panel(
                    "Unexpected analysis error",
                    f"Error inesperado durante el análisis: {exc}",
                    tone="error",
                )
            else:
                status_panel(
                    "Analysis archived",
                    f"Análisis guardado en SQLite con ID {record.id}.",
                    tone="success",
                )
                show_analysis_result(analysis)

    show_recent_records()


def show_analysis_result(analysis: ListingAnalysis) -> None:
    """Muestra un análisis con la dirección visual premium de Fase 3."""
    score = analysis.opportunity_score if analysis.opportunity_score is not None else "N/D"
    category = analysis.category or "N/D"

    st.markdown(
        f"""
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Analysis result</span>
                <span>{safe_text(analysis.marketplace)}</span>
            </div>
            <div class="lri-result-grid">
                <div class="lri-score-card">
                    <div class="lri-score-label">Opportunity score</div>
                    <div class="lri-score-number">{safe_text(score)}</div>
                    <div class="lri-category {safe_text(category)}">{safe_text(category)}</div>
                </div>
                <div>
                    <div class="lri-metric-grid">
                        {metric_card("Set ID", analysis.set_id)}
                        {metric_card("Condition", format_condition(analysis.condition))}
                        {metric_card("Fair price", format_eur(analysis.fair_price_eur))}
                        {metric_card("Asking price", format_eur(analysis.asking_price_eur))}
                        {metric_card("Buy shipping", format_eur(analysis.shipping_eur))}
                        {metric_card("Net margin", format_eur(analysis.net_margin_eur))}
                    </div>
                    <div class="lri-detail-list">
                        <div class="lri-detail-row"><span>URL</span><strong>{safe_text(analysis.url)}</strong></div>
                        <div class="lri-detail-row"><span>Gross margin</span><strong>{safe_text(format_eur(analysis.gross_margin_eur))}</strong></div>
                        <div class="lri-detail-row"><span>Notes</span><strong>{safe_text(analysis.notes)}</strong></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    show_risk_flags(analysis)
    show_margin_breakdown(analysis)


def show_risk_flags(analysis: ListingAnalysis) -> None:
    """Muestra riesgos detectados como etiquetas sobrias."""
    if analysis.risk_flags:
        pills = "".join(
            f'<span class="lri-risk-pill">{safe_text(risk_flag)}</span>'
            for risk_flag in analysis.risk_flags
        )
    else:
        pills = '<span class="lri-neutral-pill">Sin riesgos relevantes detectados</span>'

    st.markdown(
        f"""
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Risk reading</span>
                <span>LLM extraction</span>
            </div>
            <div class="lri-risk-list">{pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_margin_breakdown(analysis: ListingAnalysis) -> None:
    """Muestra el desglose explicable del margen neto."""
    breakdown = build_margin_breakdown(
        asking_price_eur=analysis.asking_price_eur,
        shipping_eur=analysis.shipping_eur,
        fair_price_eur=analysis.fair_price_eur,
    )
    steps = [
        ("Acquisition", format_eur(breakdown["acquisition_cost"])),
        ("Fair price", format_eur(breakdown["fair_price_eur"])),
        ("Fees", format_eur(breakdown["selling_fees"])),
        ("Outbound", format_eur(breakdown["shipping_out"])),
        ("Net revenue", format_eur(breakdown["net_revenue"])),
        ("Net margin", format_eur(breakdown["net_margin_eur"])),
    ]
    step_html = "".join(
        f'<div class="lri-breakdown-step">'
        f'<div class="label">{safe_text(label)}</div>'
        f'<div class="value">{safe_text(value)}</div>'
        f'</div>'
        for label, value in steps
    )

    st.markdown(
        f"""
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Margin architecture</span>
                <span>net = fair price - fees - outbound - acquisition</span>
            </div>
            <div class="lri-breakdown">{step_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def recent_active_records() -> list[ListingAnalysisRecord]:
    """Devuelve registros recientes útiles para tabla y detalle."""
    return [
        record
        for record in list_recent_listings(limit=20)
        if record.status != "discarded"
    ]


def show_recent_records() -> None:
    """Muestra la tabla de últimos análisis guardados."""
    st.markdown(
        """
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Recent intelligence</span>
                <span>SQLite archive</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    records = recent_active_records()
    recent_rows = records_as_rows(records)
    if recent_rows:
        show_saved_analysis_detail(records)
        st.markdown(
            """
            <div class="lri-table-note">
                Recent listings are kept intentionally simple: enough context to scan quality,
                without turning this phase into a dashboard.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(
            recent_rows,
            hide_index=True,
            width="stretch",
            height=310,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "category": st.column_config.TextColumn("Category"),
                "score": st.column_config.NumberColumn("Score", width="small"),
                "set_id": st.column_config.TextColumn("Set"),
                "condition": st.column_config.TextColumn("Condition"),
                "asking_price_eur": st.column_config.NumberColumn(
                    "Asking",
                    format="%.2f EUR",
                ),
                "net_margin_eur": st.column_config.NumberColumn(
                    "Net margin",
                    format="%.2f EUR",
                ),
                "marketplace": st.column_config.TextColumn("Marketplace"),
            },
        )
    else:
        status_panel(
            "No archived intelligence yet",
            "Cuando analices tu primer listing, aparecerá aquí como registro local en SQLite.",
            tone="empty",
        )


def records_as_rows(records: list[ListingAnalysisRecord]) -> list[dict[str, object]]:
    """Convierte registros concretos en filas simples para Streamlit."""
    return [
        {
            "id": record.id,
            "category": record.category,
            "score": record.opportunity_score,
            "set_id": record.set_id,
            "condition": format_condition(record.condition),
            "asking_price_eur": record.asking_price_eur,
            "net_margin_eur": record.net_margin_eur,
            "marketplace": record.marketplace,
        }
        for record in records[:12]
    ]


def show_saved_analysis_detail(records: list[ListingAnalysisRecord]) -> None:
    """Permite revisar un análisis guardado sin añadir nueva lógica de negocio."""
    options = {
        f"#{record.id} · {record.set_id} · {record.category} · score {record.opportunity_score}": record
        for record in records[:12]
    }
    st.markdown(
        """
        <div class="lri-inspector-panel">
            <div>
                <div class="lri-inspector-eyebrow">Archive inspector</div>
                <div class="lri-inspector-title">Review one saved analysis</div>
            </div>
            <div class="lri-inspector-note">SQLite detail</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_label = st.selectbox(
        "Inspect archived analysis",
        options=list(options.keys()),
        label_visibility="collapsed",
    )
    selected_record = options[selected_label]
    show_record_detail(selected_record)


def show_record_detail(record: ListingAnalysisRecord) -> None:
    """Muestra detalle premium de un registro persistido."""
    risk_flags = record.risk_flags or []
    risks_html = (
        "".join(f'<span class="lri-risk-pill">{safe_text(flag)}</span>' for flag in risk_flags)
        if risk_flags
        else '<span class="lri-neutral-pill">Sin riesgos relevantes archivados</span>'
    )
    st.markdown(
        f"""
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Archived detail</span>
                <span>record #{safe_text(record.id)}</span>
            </div>
            <div class="lri-result-grid compact">
                <div class="lri-score-card">
                    <div class="lri-score-label">Archived score</div>
                    <div class="lri-score-number">{safe_text(record.opportunity_score)}</div>
                    <div class="lri-category {safe_text(record.category)}">{safe_text(record.category)}</div>
                </div>
                <div>
                    <div class="lri-metric-grid">
                        {metric_card("Set ID", record.set_id)}
                        {metric_card("Condition", format_condition(record.condition))}
                        {metric_card("Marketplace", record.marketplace)}
                        {metric_card("Asking price", format_eur(record.asking_price_eur))}
                        {metric_card("Fair price", format_eur(record.fair_price_eur))}
                        {metric_card("Net margin", format_eur(record.net_margin_eur))}
                    </div>
                    <div class="lri-risk-list">{risks_html}</div>
                    <div class="lri-detail-list">
                        <div class="lri-detail-row"><span>URL</span><strong>{safe_text(record.url)}</strong></div>
                        <div class="lri-detail-row"><span>Gross margin</span><strong>{safe_text(format_eur(record.gross_margin_eur))}</strong></div>
                        <div class="lri-detail-row"><span>Notes</span><strong>{safe_text(record.notes)}</strong></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def show_about() -> None:
    """Explica método, alcance y límites del producto."""
    lego_logo_uri = image_data_uri(LEGO_LOGO_PATH)
    st.markdown(
        f"""
        <section class="lri-hero">
            <div class="lri-hero-copy">
                <div class="lri-kicker">Method & scope</div>
                <h1 class="lri-title">A transparent system, not a black box.</h1>
                <p class="lri-subtitle">
                    The product combines a small local catalog, manual fair price references,
                    LLM extraction and explicit scoring rules. Every result should be explainable.
                </p>
            </div>
            <div class="lri-object-stage" aria-hidden="true">
                <div class="lri-logo-plinth">
                    <img class="lri-lego-logo" src="{lego_logo_uri}" alt="LEGO logo" />
                </div>
            </div>
        </section>
        <div class="lri-panel">
            <div class="lri-section-label">
                <span>Pipeline</span>
                <span>Phase 2 core</span>
            </div>
            <div class="lri-pipeline">
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">01</div>
                    <div class="lri-step-title">Capture</div>
                    <div class="lri-step-copy">Download one listing HTML with a conservative parser.</div>
                </div>
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">02</div>
                    <div class="lri-step-title">Extract</div>
                    <div class="lri-step-copy">Anthropic structures title, set ID, condition and risks.</div>
                </div>
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">03</div>
                    <div class="lri-step-title">Identify</div>
                    <div class="lri-step-copy">The set is matched against the local CSV catalog.</div>
                </div>
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">04</div>
                    <div class="lri-step-title">Price</div>
                    <div class="lri-step-copy">Manual fair price references anchor the estimate.</div>
                </div>
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">05</div>
                    <div class="lri-step-title">Score</div>
                    <div class="lri-step-copy">Margins, risk and marketplace produce a score.</div>
                </div>
                <div class="lri-pipeline-step">
                    <div class="lri-step-number">06</div>
                    <div class="lri-step-title">Archive</div>
                    <div class="lri-step-copy">SQLite stores the analyzed listing locally.</div>
                </div>
            </div>
        </div>
        <div class="lri-editorial-grid">
            <div class="lri-editorial-card">
                <div class="lri-card-index">Scoring</div>
                <div class="lri-card-title">Simple enough to defend.</div>
                <div class="lri-card-copy">
                    Net margin drives the score. Risk flags reduce confidence. GREEN requires
                    both a strong score and positive absolute margin.
                </div>
            </div>
            <div class="lri-editorial-card">
                <div class="lri-card-index">Limitations</div>
                <div class="lri-card-title">Marketplaces are messy.</div>
                <div class="lri-card-copy">
                    Listings can disappear, HTML can change and eBay may block requests.
                    These are documented constraints, not hidden failures.
                </div>
            </div>
            <div class="lri-editorial-card">
                <div class="lri-card-index">Status</div>
                <div class="lri-card-title">Ready for product polish.</div>
                <div class="lri-card-copy">
                    Phase 2 is validated. Phase 3A focuses on experience, presentation and
                    confidence without changing the core pipeline.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="LEGO Resale Intelligence",
    page_icon="L",
    layout="wide",
)
apply_global_styles()
show_topline()

overview_tab, analyze_tab, about_tab = show_navigation()
with overview_tab:
    show_overview()
with analyze_tab:
    show_analyze()
with about_tab:
    show_about()
