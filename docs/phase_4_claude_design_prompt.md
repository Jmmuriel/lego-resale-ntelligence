# Prompt maestro para Claude Design - Case Study PDF

## Objetivo

Crear un PDF/case study visual, premium y vendible para el proyecto personal **LEGO Resale Intelligence**.

Este PDF pertenece a la **Fase 4 - Documentación & presentación** de la guía maestra del proyecto.

Debe sentirse como una pieza de portfolio seria, no como documentación técnica plana.

## Prompt para copiar en Claude Design

```text
Quiero que diseñes un case study PDF visual y premium para mi proyecto personal:

LEGO Resale Intelligence

IMPORTANTE:
- Es un proyecto personal/educativo, no afiliado oficialmente con LEGO.
- No copies literalmente ningún diseño de referencia.
- Usa las referencias como inspiración visual: brandbook, editorial premium, producto digital, museo/coleccionismo.
- El resultado debe sentirse vendible, serio y de portfolio.
- No quiero una presentación infantil.
- No quiero un PDF genérico tipo informe universitario.
- Quiero una pieza visual con dirección de arte clara.

FORMATO:
- PDF horizontal 16:9 o A4 landscape.
- 10-12 páginas máximo.
- Muy visual, poco texto por página.
- Grandes capturas, jerarquía tipográfica fuerte, mucho espacio en blanco.
- Estética premium: museo + intelligence tool + LEGO-inspired brand system.

REFERENCIAS VISUALES A INTERPRETAR:
1. Manual de Identidad LEGO / brandbook:
   - inspiración: sistema visual, reglas, retícula, paleta, piezas de marca.
   - tomar: disciplina editorial, bloques de color, uso fuerte de rojo/amarillo/negro/blanco.
   - evitar: copiar páginas exactas.

2. Levi's x LEGO Fall 2022 Collaboration:
   - inspiración: colaboración premium, producto físico, creatividad modular, piezas coleccionables.
   - tomar: sensación de objeto, textura, composición tipo campaña.
   - evitar: parecer moda o campaña Levi's.

3. LEGO Museum / piezas tipo museo:
   - inspiración: objeto expuesto, vitrina, colección, archivo.
   - tomar: sensación de display, orden, profundidad visual.

4. CalmMate / DESCOM case studies:
   - inspiración: narrativa de producto y UI/UX case study.
   - tomar: storytelling claro, problema -> solución -> sistema -> resultado.

DIRECCIÓN VISUAL:
- Minimalismo premium con acentos LEGO.
- Fondo principal cálido/off-white.
- Rojo LEGO como acento fuerte, no como fondo constante.
- Amarillo LEGO solo para highlights y detalles.
- Negro para contraste, titulares y componentes de score.
- Tratar los datos como piezas de colección.
- Usar capturas grandes dentro de marcos tipo vitrina o lámina editorial.
- Sensación de manual de identidad + producto SaaS + museo de coleccionismo.

PALETA RECOMENDADA:
- LEGO-inspired red: #E3000B
- LEGO-inspired yellow: #FFED00
- Black: #111111
- White: #FFFFFF
- Warm background: #F4F1EA
- Surface: #FFFDF8
- Muted text: #6F6A61
- Success green: #116B4F
- Warning yellow: #D6A900

TIPOGRAFÍA:
- Usar una sans-serif moderna y muy limpia.
- Recomendadas: Inter, Neue Haas Grotesk, Helvetica Now, Space Grotesk o similar.
- Titulares grandes, compactos y con mucho peso.
- Labels pequeños en uppercase con tracking amplio.
- Usar monospace solo para mini fragmentos técnicos o pipeline.

TONO DE COPY:
- Profesional, claro y seguro.
- No exagerar.
- Evitar marketing vacío.
- Debe sonar a product engineer que sabe explicar qué construyó.
- Puede estar en inglés para portfolio internacional.

TÍTULO PRINCIPAL:
LEGO Resale Intelligence

SUBTÍTULO:
A premium resale intelligence tool for retired LEGO listings.

ONE-LINER:
An end-to-end Streamlit application that captures real marketplace listings, extracts structured data with Anthropic, identifies retired LEGO sets, calculates margins, scores buying opportunities and archives results locally.

DISCLAIMER PEQUEÑO:
Personal educational project. Not affiliated with or endorsed by the LEGO Group.

ESTRUCTURA DEL PDF:

PAGE 1 - Cover
- Título grande: LEGO Resale Intelligence
- Subtítulo: A premium resale intelligence tool for retired LEGO listings.
- Visual: usar captura `phase3b_desktop_overview.png` o close-up `phase3b_closeup_hero_logo.png`.
- Añadir badges pequeños:
  - Python
  - Streamlit
  - Anthropic
  - SQLite
  - Phase 4 Case Study

PAGE 2 - The Problem
Título:
Marketplace listings are noisy. Good opportunities are easy to miss.

Texto corto:
Retired LEGO sets can be valuable, but marketplace listings are inconsistent: incomplete titles, unclear condition, missing set IDs, unstable URLs and prices that are hard to compare. A buyer needs a fast way to separate signal from noise before making a decision.

Visual:
- Usar una composición editorial con palabras clave:
  - asking price
  - fair price
  - set ID
  - condition
  - risk flags
  - net margin

PAGE 3 - The Product
Título:
From one URL to an opportunity score.

Texto:
The app takes a real listing URL, captures its HTML, extracts structured information, matches the LEGO set against a local catalog, estimates fair price, calculates net margin and stores the analysis in SQLite.

Visual:
Usar captura `phase3b_desktop_analyze.png`.

PAGE 4 - Architecture
Título:
A simple, explainable pipeline.

Diagrama visual:
URL
→ capture.py
→ parse_listing_html
→ extract.py / Anthropic
→ identify.py / catalog.csv
→ pricing_reference.py
→ scoring.py
→ db.py / SQLite
→ Streamlit UI

Texto lateral:
The architecture is intentionally small: no FastAPI, no React, no Postgres, no Docker. The goal was a defendable v1 that a junior developer can understand, test and iterate.

PAGE 5 - Intelligence Layer
Título:
Scoring is explicit, not magic.

Contenido:
- Gross margin = fair price - acquisition cost.
- Net margin accounts for estimated selling fees and outbound shipping.
- Opportunity score combines margin strength, risk flags and marketplace context.
- GREEN requires both strong score and positive absolute margin.

Visual:
Usar `phase3b_closeup_archived_score.png`.

PAGE 6 - Product Experience
Título:
Premium UI, still grounded in a real workflow.

Texto:
Phase 3 transformed the prototype into a polished Streamlit experience with three sections: Overview, Analyze and About. The UI uses an editorial layout, restrained LEGO-inspired accents and clear states for real pipeline outcomes.

Visual:
Usar `phase3b_desktop_overview.png` y una pequeña superposición de `phase3b_desktop_about.png`.

PAGE 7 - Analyze View
Título:
Operational, clear and traceable.

Contenido breve:
- Paste listing URL.
- Run live pipeline.
- Save result locally.
- Review archived analysis.
- Inspect score, condition, price, margin and risk flags.

Visual:
Usar `phase3b_desktop_analyze_detail.png`.

PAGE 8 - Responsive Polish
Título:
Designed to hold up beyond desktop.

Texto:
The final Streamlit interface was reviewed on desktop and mobile. Layouts collapse into readable sections while preserving the premium editorial direction.

Visual:
Usar `phase3b_mobile_overview.png` y `phase3b_mobile_analyze.png` como mockups verticales.

PAGE 9 - Validation
Título:
Tested with real URLs, not only mock data.

Datos a mostrar:
- 20 real Wallapop URLs tested across validation rounds.
- 13 completed end-to-end successfully.
- 7 failed due to external 404/unavailable listings.
- 64 automated tests passing.
- 10 catalog sets covered.
- SQLite archival confirmed.
- Anthropic extraction confirmed.

Nota:
Failures were documented as external marketplace constraints, not hidden errors.

PAGE 10 - What Was Built
Título:
Built as a serious v1, not an over-engineered system.

Mostrar stack:
- Python
- Streamlit
- Pydantic v2
- Requests
- BeautifulSoup
- Anthropic
- SQLAlchemy
- SQLite
- Pytest
- python-dotenv

Mostrar módulos:
- capture.py
- extract.py
- identify.py
- pricing_reference.py
- scoring.py
- pipeline.py
- db.py
- app/main.py

PAGE 11 - Limitations & Next Steps
Título:
Clear limits make the product more credible.

Limitations:
- Local catalog is still small.
- Fair prices are manual.
- HTML parsing is basic.
- Marketplaces can block or remove listings.
- Score is explainable, not a financial guarantee.

Next steps:
- Expand catalog coverage.
- Improve fair price references.
- Validate more real listings.
- Consider public Streamlit deploy.
- Prepare demo video and LinkedIn post.

PAGE 12 - Closing
Título:
From noisy marketplace listings to a focused buying signal.

Closing copy:
LEGO Resale Intelligence is a personal product engineering project built to show end-to-end thinking: data capture, LLM extraction, structured modeling, scoring, persistence, testing and premium product presentation.

Footer:
Built by Juan Manuel Muriel Mora
Python · Product Engineering · UI polish · AI-assisted workflows

IMAGES TO USE:
Upload/use these exact screenshots:

1. docs/screenshots/phase3b_desktop_overview.png
2. docs/screenshots/phase3b_desktop_analyze.png
3. docs/screenshots/phase3b_desktop_analyze_detail.png
4. docs/screenshots/phase3b_desktop_about.png
5. docs/screenshots/phase3b_mobile_overview.png
6. docs/screenshots/phase3b_mobile_analyze.png
7. docs/screenshots/phase3b_mobile_about.png
8. docs/screenshots/phase3b_closeup_hero_logo.png
9. docs/screenshots/phase3b_closeup_archived_score.png
10. docs/screenshots/phase3b_closeup_mobile_archive.png

DESIGN RULES:
- Do not overcrowd pages.
- One main idea per page.
- Use large screenshots.
- Use red/yellow/black sparingly and deliberately.
- Keep most backgrounds warm white/off-white.
- Use subtle grid lines or modular blocks inspired by LEGO studs/pieces.
- Avoid childish toy aesthetics.
- Avoid rainbow color overload.
- Avoid generic dashboard look.
- Avoid too much text.
- Make it feel like a premium case study someone would save on Behance.

FINAL OUTPUT:
- A polished PDF case study.
- Visual language: editorial brandbook + product case study.
- Must be suitable for portfolio, LinkedIn and job applications.
```

## Notas para preparar assets antes de usar Claude Design

Subir a Claude Design las 10 imágenes listadas arriba.

Si Claude Design no puede acceder a rutas locales, subirlas manualmente desde:

```text
/Users/juanmanuelmurielmora/Desktop/lego-resale-intelligence/docs/screenshots/
```

## Información factual del proyecto

### Nombre

LEGO Resale Intelligence

### Descripción corta

Herramienta personal de e-commerce intelligence para analizar listings de LEGO descatalogado, estimar márgenes y priorizar oportunidades de compra.

### Estado

- Fase 2 cerrada como v1 técnica local.
- Fase 3 cerrada como experiencia premium en Streamlit.
- Fase 4 actual: documentación y presentación para portfolio.

### Stack

- Python
- Streamlit
- Pydantic v2
- Requests
- BeautifulSoup
- Anthropic
- SQLAlchemy
- SQLite
- Pytest
- python-dotenv

### Resultados verificables

- 64 tests automatizados pasando.
- 20 URLs reales probadas en validaciones.
- 13 flujos end-to-end completados.
- 7 fallos externos documentados por listings no accesibles.
- 10 sets en catálogo local.
- Guardado en SQLite confirmado.
- Extracción con Anthropic confirmada.

### Limitaciones honestas

- Catálogo local pequeño.
- Fair prices manuales.
- Parser HTML básico.
- Marketplaces pueden bloquear o borrar listings.
- Score explicable, no predicción financiera definitiva.

## Inspiración estudiada

- Behance: Manual de Identidad Lego.
- Behance: Levi's X LEGO Fall 2022 Collaboration.
- Behance: Kids Choice Awards | LEGO Super Mario.
- Behance: CalmMate AI Anxiety Companion app case study.
- Behance: DESCOM Web Design Case Study.

Lectura visual:

- Tomar del brandbook LEGO: disciplina, paleta primaria, retícula, sensación de manual.
- Tomar de Levi's x LEGO: objeto de colección, colaboración premium, modularidad.
- Tomar de Kids Choice / LEGO Super Mario solo la profundidad visual; evitar el tono infantil.
- Tomar de CalmMate/DESCOM la narrativa de case study y la progresión problema-solución-producto.

## Recomendación final

Claude Design debe crear una pieza más visual que técnica. El código ya existe; el PDF debe vender:

1. el problema;
2. la solución;
3. el criterio de ingeniería;
4. el producto visual;
5. la capacidad de Juan para cerrar una v1 defendible.
