# Prompt ultra visual para Claude Design

Este es el prompt recomendado para crear un case study PDF con estética premium tipo Behance.

Antes de pegarlo en Claude Design, sube estas 10 capturas:

```text
docs/screenshots/phase3b_desktop_overview.png
docs/screenshots/phase3b_desktop_analyze.png
docs/screenshots/phase3b_desktop_analyze_detail.png
docs/screenshots/phase3b_desktop_about.png
docs/screenshots/phase3b_mobile_overview.png
docs/screenshots/phase3b_mobile_analyze.png
docs/screenshots/phase3b_mobile_about.png
docs/screenshots/phase3b_closeup_hero_logo.png
docs/screenshots/phase3b_closeup_archived_score.png
docs/screenshots/phase3b_closeup_mobile_archive.png
```

## Prompt final

```text
Actúa como un equipo senior formado por:
- Creative Director
- Editorial Designer
- UI/UX Case Study Designer
- Brand Systems Designer
- Product Storyteller

Quiero que diseñes un PDF case study extremadamente visual, premium y publicable en Behance para mi proyecto:

LEGO Resale Intelligence

OBJETIVO PRINCIPAL
Crear una pieza de portfolio que parezca diseñada por un estudio premium: visual, editorial, memorable, clara y profesional.

Este PDF debe vender el proyecto como una v1 seria de product engineering, no como un informe técnico.

IMPORTANTE
- Es un proyecto personal/educativo.
- No está afiliado oficialmente con LEGO.
- No copies literalmente ninguna referencia.
- No inventes funcionalidades que no existen.
- No conviertas esto en un dashboard genérico.
- No hagas un documento escolar.
- No llenes páginas de texto.
- Cada página debe funcionar visualmente incluso si alguien solo la mira 3 segundos.

FORMATO
- PDF horizontal 16:9, estilo Behance case study.
- 12 páginas máximo.
- Diseño editorial de alto impacto.
- Mucho espacio en blanco.
- Capturas grandes.
- Composiciones tipo brandbook/product launch.
- Visual rhythm: alternar páginas hero, páginas de sistema, páginas técnicas simplificadas y páginas con mockups.

REFERENCIAS VISUALES

Usa estas URLs como referencia de estilo, NO para copiar:

1. Manual de Identidad Lego
https://www.behance.net/gallery/169710979/Manual-de-Identidad-Lego

Tomar:
- disciplina de brandbook;
- retículas limpias;
- bloques de color;
- jerarquía editorial;
- sistema visual consistente;
- uso potente de rojo, amarillo, negro y blanco.

2. Levi's X LEGO Fall 2022 Collaboration
https://www.behance.net/gallery/158101173/Levis-X-LEGO-Fall-2022-Collaboration

Tomar:
- sensación de colaboración premium;
- objeto de colección;
- producto tratado como pieza física;
- composición de campaña;
- profundidad visual y textura.

3. CalmMate AI Anxiety Companion UI/UX Case Study
https://www.behance.net/gallery/241701875/CalmMate-AI-Anxiety-Companion-app-%28UIUX-Case-Study%29

Tomar:
- narrativa UI/UX clara;
- estructura problema -> solución -> producto;
- pantallas presentadas con intención;
- sensación moderna de case study.

4. DESCOM Web Design Case Study
https://www.behance.net/gallery/247299207/DESCOM-Web-Design-Case-Study

Tomar:
- composición web premium;
- screenshots grandes;
- secciones limpias;
- ritmo de presentación profesional.

DIRECCIÓN ARTÍSTICA

Concepto visual:
"A museum-grade intelligence system for retired LEGO resale opportunities."

La estética debe mezclar:
- museo de coleccionismo;
- manual de identidad;
- producto SaaS premium;
- inteligencia de mercado;
- lenguaje modular inspirado en piezas LEGO.

Debe sentirse:
- premium;
- minimalista;
- editorial;
- sobrio;
- creativo;
- coleccionable;
- técnico pero accesible.

No debe sentirse:
- infantil;
- barato;
- genérico;
- sobrecargado;
- académico;
- como plantilla de PowerPoint;
- como dashboard financiero común.

PALETA

Usa una paleta LEGO-inspired pero sofisticada:

- Red primary: #E3000B
- Yellow accent: #FFED00
- Black: #111111
- White: #FFFFFF
- Warm museum background: #F4F1EA
- Surface: #FFFDF8
- Muted grey/brown: #6F6A61
- Success green: #116B4F
- Warning yellow: #D6A900

Reglas de color:
- El fondo principal debe ser warm white/off-white.
- El rojo debe aparecer como acento fuerte, no como fondo constante.
- El amarillo debe usarse poco, como highlight.
- El negro debe dar peso, contraste y sofisticación.
- Evitar arcoíris.
- Evitar colores infantiles.

TIPOGRAFÍA

Usa una sans-serif premium:
- Inter
- Neue Haas Grotesk
- Helvetica Now
- Space Grotesk
- Söhne
- o similar.

Jerarquía:
- Titulares enormes, compactos y con mucho peso.
- Subtítulos cortos.
- Labels en uppercase con tracking amplio.
- Cuerpo de texto muy reducido.
- Datos numéricos grandes, tratados como piezas visuales.

No usar tipografía infantil, redondeada en exceso o decorativa.

SISTEMA GRÁFICO

Crear un lenguaje visual propio con:
- retículas modulares;
- líneas finas;
- marcos tipo vitrina;
- placas/cards tipo piezas coleccionables;
- pequeños bloques rojos/amarillos como acentos;
- sombras suaves;
- screenshots flotando como objetos;
- close-ups tipo fotografía de producto;
- números grandes;
- micro-etiquetas técnicas.

Puedes usar patrones sutiles inspirados en studs LEGO, pero MUY discretos.
No crear ilustraciones infantiles.

COPY GENERAL

Nombre:
LEGO Resale Intelligence

Subtítulo:
A premium resale intelligence tool for retired LEGO listings.

One-liner:
An end-to-end Streamlit application that captures real marketplace listings, extracts structured data with Anthropic, identifies retired LEGO sets, calculates margins, scores buying opportunities and archives results locally.

Disclaimer:
Personal educational project. Not affiliated with or endorsed by the LEGO Group.

STACK
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

RESULTADOS VERIFICABLES
- 64 automated tests passing.
- 20 real Wallapop URLs tested.
- 13 completed end-to-end successfully.
- 7 failed due to external unavailable listings / 404.
- 10 catalog sets covered.
- SQLite archival confirmed.
- Anthropic extraction confirmed.
- Desktop and mobile UI reviewed.

LIMITACIONES HONESTAS
- Local catalog is still small.
- Fair prices are manual.
- HTML parsing is basic.
- Marketplaces can block or remove listings.
- Score is explainable, not a financial guarantee.

IMÁGENES ADJUNTAS
Usa las imágenes adjuntas con estos nombres:

1. phase3b_desktop_overview.png
2. phase3b_desktop_analyze.png
3. phase3b_desktop_analyze_detail.png
4. phase3b_desktop_about.png
5. phase3b_mobile_overview.png
6. phase3b_mobile_analyze.png
7. phase3b_mobile_about.png
8. phase3b_closeup_hero_logo.png
9. phase3b_closeup_archived_score.png
10. phase3b_closeup_mobile_archive.png

IMPORTANTE SOBRE LAS IMÁGENES
- No las deformes.
- No las estires.
- Mantén proporciones.
- Úsalas como producto real.
- Puedes enmarcarlas en mockups, vitrinas, floating frames o layouts editoriales.
- Las mobile screenshots deben parecer mockups verticales premium.
- Las desktop screenshots deben respirar y verse grandes.

ESTRUCTURA DEL PDF

PAGE 1 — HERO COVER

Objetivo visual:
Impacto inmediato tipo Behance.

Composición:
- Fondo warm off-white.
- Título enorme: LEGO Resale Intelligence.
- Subtítulo debajo.
- Usar `phase3b_closeup_hero_logo.png` como objeto visual principal o detalle.
- Incluir una gran captura `phase3b_desktop_overview.png` en segundo plano o como mockup.
- Añadir badges pequeños:
  Python · Streamlit · Anthropic · SQLite · Product Engineering

Copy:
LEGO Resale Intelligence
A premium resale intelligence tool for retired LEGO listings.

Footer pequeño:
Personal educational project. Not affiliated with or endorsed by the LEGO Group.

PAGE 2 — PROBLEM

Objetivo visual:
Hacer que el problema se entienda rápido.

Título:
Marketplace listings are noisy. Good opportunities are easy to miss.

Copy:
Retired LEGO sets can be valuable, but marketplace listings are inconsistent: incomplete titles, unclear condition, missing set IDs, unstable URLs and prices that are hard to compare.

Visual:
Crear una composición modular con palabras clave:
set ID · asking price · fair price · condition · risk flags · net margin · score

Estilo:
Como piezas sueltas que el sistema ordena.

PAGE 3 — PRODUCT PROMISE

Título:
From one URL to an opportunity score.

Copy:
The app turns a real listing URL into a structured buying signal: fair price, net margin, risk flags, opportunity score and local archive.

Visual:
Usar `phase3b_desktop_analyze.png` grande.

Composición:
Screenshot como pieza central.
Añadir 4 labels alrededor:
Capture
Extract
Score
Archive

PAGE 4 — ARCHITECTURE

Título:
A simple, explainable pipeline.

Visual:
Diagrama modular grande, no aburrido.

Pipeline:
URL
→ capture.py
→ parse_listing_html
→ extract.py / Anthropic
→ identify.py / catalog.csv
→ pricing_reference.py
→ scoring.py
→ db.py / SQLite
→ Streamlit UI

Copy lateral:
The architecture is intentionally small: no FastAPI, no React, no Postgres, no Docker. The goal was a defendable v1 that a junior developer can understand, test and iterate.

Estilo:
Cada módulo debe parecer una pieza/bloque del sistema.

PAGE 5 — INTELLIGENCE LAYER

Título:
Scoring is explicit, not magic.

Visual:
Usar `phase3b_closeup_archived_score.png` muy grande.

Copy breve:
Gross margin = fair price - acquisition cost.
Net margin accounts for fees and outbound shipping.
Opportunity score combines margin strength, risk flags and marketplace context.

Data highlight:
97 score
GREEN
240 EUR net margin

PAGE 6 — PRODUCT EXPERIENCE

Título:
Premium UI, grounded in a real workflow.

Copy:
Phase 3 transformed the prototype into a polished Streamlit experience with three sections: Overview, Analyze and About.

Visual:
Usar `phase3b_desktop_overview.png` como screenshot hero.
Añadir pequeños fragments/crops de la UI si queda bien.

Estilo:
Producto digital premium sobre una mesa/vitrina editorial.

PAGE 7 — ANALYZE VIEW

Título:
Operational, clear and traceable.

Copy bullets:
- Paste listing URL.
- Run live pipeline.
- Save result locally.
- Review archived analysis.
- Inspect score, condition, price, margin and risk flags.

Visual:
Usar `phase3b_desktop_analyze_detail.png` grande.

Debe sentirse como:
Una herramienta real, no solo una landing.

PAGE 8 — RESPONSIVE POLISH

Título:
Designed to hold up beyond desktop.

Copy:
The final Streamlit interface was reviewed on desktop and mobile. Layouts collapse into readable sections while preserving the premium editorial direction.

Visual:
Usar:
- `phase3b_mobile_overview.png`
- `phase3b_mobile_analyze.png`
- `phase3b_mobile_about.png`

Composición:
Tres mockups verticales, como dispositivos o láminas.

PAGE 9 — VALIDATION

Título:
Tested with real URLs, not only mock data.

Mostrar números grandes:
64 tests passing
20 real URLs tested
13 end-to-end successes
7 external failures documented
10 catalog sets

Copy:
Failures were documented as external marketplace constraints, not hidden errors.

Visual:
Usar módulos numéricos grandes, tipo brand system.

PAGE 10 — WHAT WAS BUILT

Título:
Built as a serious v1, not an over-engineered system.

Visual:
Mapa de módulos:
capture.py
extract.py
identify.py
pricing_reference.py
scoring.py
pipeline.py
db.py
app/main.py
app/styles.py

Stack badges:
Python · Streamlit · Anthropic · SQLite · SQLAlchemy · Pydantic · Pytest

Estilo:
Técnico pero visual. No hacer bloque de texto.

PAGE 11 — LIMITATIONS & NEXT STEPS

Título:
Clear limits make the product more credible.

Limitations:
- Local catalog is still small.
- Fair prices are manual.
- HTML parsing is basic.
- Marketplaces can block or remove listings.
- Score is explainable, not a financial guarantee.

Next steps:
- Final README.
- Architecture diagram.
- 2-minute demo video.
- Streamlit Community Cloud deploy.
- LinkedIn post.
- CV bullets.

Composición:
Dos columnas: limitations / next steps.

PAGE 12 — CLOSING POSTER

Objetivo:
Cerrar con fuerza visual.

Título:
From noisy marketplace listings to a focused buying signal.

Copy:
LEGO Resale Intelligence is a personal product engineering project built to show end-to-end thinking: data capture, LLM extraction, structured modeling, scoring, persistence, testing and premium product presentation.

Footer:
Built by Juan Manuel Muriel Mora
Python · Product Engineering · AI-assisted workflows · UI polish

Visual:
Usar una composición final con:
- logo close-up;
- screenshot desktop;
- pequeños bloques de datos;
- sensación de poster/cierre de caso.

REGLAS DE CALIDAD

Antes de entregar, revisa:
- ¿Parece un case study de Behance?
- ¿Hay suficiente impacto visual?
- ¿Cada página tiene una sola idea clara?
- ¿Las screenshots se ven grandes y limpias?
- ¿El texto no abruma?
- ¿La paleta es coherente?
- ¿El rojo/amarillo se usan con intención?
- ¿Se entiende problema -> solución -> producto -> validación?
- ¿Se ve premium y profesional?
- ¿Evita estética infantil?
- ¿Evita dashboard genérico?

NEGATIVE PROMPT

No hagas:
- informe corporativo aburrido;
- documento académico;
- demasiadas cajas de texto;
- fondos grises genéricos;
- exceso de colores;
- iconos infantiles;
- mockups falsos de features no existentes;
- diseño tipo plantilla Canva básica;
- capturas pequeñas;
- páginas saturadas;
- estética de juguetería.

FINAL OUTPUT

Entrega un PDF final pulido, visual y premium, listo para:
- portfolio;
- Behance;
- LinkedIn;
- entrevistas;
- job applications.
```
