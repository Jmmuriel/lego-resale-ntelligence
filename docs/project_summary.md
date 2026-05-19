# LEGO Resale Intelligence - resumen de V1

Fecha de cierre de referencia: 2026-05-14

Este documento resume el estado real del proyecto para poder continuar en otro chat o iniciar la V2 sin perder contexto.

## Estado general

**LEGO Resale Intelligence V1 esta terminada.**

Es una herramienta personal de e-commerce intelligence para analizar listings de LEGO descatalogado. La app convierte una URL de marketplace en una senal de compra estructurada:

- set identificado
- condicion estimada
- fair price manual
- margen bruto
- margen neto
- risk flags
- opportunity score
- categoria GREEN / AMBER / RED
- guardado en SQLite
- visualizacion en Streamlit con interfaz premium

El proyecto esta pensado como portfolio tecnico-producto: simple, explicable, visualmente cuidado y sin arquitectura innecesaria.

## Stack actual

- Python 3.11
- Streamlit
- Anthropic como proveedor LLM
- Pydantic v2
- SQLAlchemy
- SQLite
- requests
- BeautifulSoup
- pytest
- HTML/CSS custom para la capa visual

No se uso FastAPI, React, Docker, Postgres ni scraping masivo.

## Fases completadas

### Fase 1 - Scaffold inicial

Se creo la base del proyecto:

- `requirements.txt`
- `.gitignore`
- `.env.example`
- `setup.sh`
- estructura `src/`, `app/`, `data/`, `tests/`, `docs/`
- app minima en Streamlit
- README inicial

### Fase 2 - Pipeline tecnico

La Fase 2 quedo cerrada segun la guia maestra.

Incluye:

- `src/capture.py`: descarga HTML de una URL individual y parsea datos basicos.
- `src/extract.py`: extraccion estructurada con Anthropic hacia `ListingExtraction`.
- `src/identify.py`: matching contra `data/catalog.csv`.
- `data/catalog.csv`: catalogo local inicial de sets retirados.
- `src/pricing_reference.py`: referencias manuales de fair price por set y condicion.
- `src/scoring.py`: calculo de margenes, score y categoria.
- `src/db.py`: SQLite + CRUD basico con SQLAlchemy.
- `src/pipeline.py`: orquestador end-to-end.
- tests unitarios e integracion con mocks donde aplica.
- validacion manual con URLs reales.

Flujo principal:

```text
URL
 -> capture.py
 -> extract.py
 -> identify.py
 -> pricing_reference.py
 -> scoring.py
 -> db.py
 -> app/main.py
```

Funcion clave:

```python
analyze_listing_url(url: str) -> ListingAnalysis
```

Tambien existe flujo con guardado:

```python
analyze_and_save_listing_url(...)
```

### Fase 3 - Interfaz premium Streamlit

La Fase 3 quedo cerrada como experiencia premium dentro de Streamlit, sin cambiar la arquitectura.

Incluye:

- secciones `Overview`, `Analyze`, `About`
- landing editorial premium
- vista de analisis funcional
- tabla simple de ultimos analisis
- vista detalle de analisis guardado
- estados de error/loading/empty mas cuidados
- responsive desktop/mobile
- CSS custom en `app/styles.py`
- logo local en `app/assets/lego_logo.png`

La direccion visual buscada fue:

- minimalismo premium
- museo / coleccion
- intelligence tool
- no infantil
- rojo/amarillo/negro usados de forma controlada
- mucho espacio blanco
- jerarquia tipografica fuerte

### Fase 4 - Documentacion y presentacion

La Fase 4 quedo avanzada/cerrada para portfolio.

Incluye:

- README serio y actualizado.
- capturas finales en `docs/screenshots/`.
- carpeta de assets seleccionados para case study.
- prompt ultra detallado para Claude Design:
  - `docs/phase_4_claude_design_prompt.md`
  - `docs/phase_4_claude_design_prompt_ultra.md`
- case study visual creado directamente en HTML/PDF:
  - `docs/case_study/lego_resale_intelligence_case_study.html`
  - `docs/case_study/lego_resale_intelligence_case_study.pdf`
- paginas PNG para Behance:
  - `docs/case_study/preview/page_01.png`
  - ...
  - `docs/case_study/preview/page_12.png`

Nota: se elimino una slide de "Limits & Next Steps" porque el usuario no queria que apareciera en el PDF final.

## Archivos clave

### App

- `app/main.py`: interfaz Streamlit principal.
- `app/styles.py`: CSS custom premium.
- `app/assets/lego_logo.png`: logo usado en la app.

### Core Python

- `src/models.py`: modelos Pydantic.
- `src/capture.py`: captura y parser HTML basico.
- `src/extract.py`: extraccion LLM con Anthropic.
- `src/identify.py`: matching contra catalogo.
- `src/pricing_reference.py`: fair prices manuales.
- `src/scoring.py`: margenes, score y categoria.
- `src/db.py`: persistencia SQLite.
- `src/pipeline.py`: flujo end-to-end.
- `src/manual_analysis.py`: flujo manual de analisis.
- `src/placeholders.py`: demo/mock legacy para pruebas controladas.

### Datos

- `data/catalog.csv`: catalogo local.

### Tests

- `tests/test_capture.py`
- `tests/test_db.py`
- `tests/test_extract.py`
- `tests/test_identify.py`
- `tests/test_main_logic.py`
- `tests/test_manual_analysis.py`
- `tests/test_models.py`
- `tests/test_pipeline.py`
- `tests/test_pricing_reference.py`
- `tests/test_scoring.py`

### Documentacion

- `README.md`
- `docs/phase_2_validation.md`
- `docs/phase_2_extended_validation.md`
- `docs/phase_3_closure.md`
- `docs/phase_3_design_direction.md`
- `docs/phase_3_readiness.md`
- `docs/phase_4_claude_design_prompt_ultra.md`
- `docs/case_study/lego_resale_intelligence_case_study.pdf`

## Comandos utiles

Crear/activar entorno:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ejecutar app:

```bash
streamlit run app/main.py
```

Ejecutar tests:

```bash
pytest
```

Variables esperadas:

```env
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
DATABASE_URL=
```

Si `DATABASE_URL` esta vacio, se usa SQLite local.

## Estado funcional de V1

La V1 permite:

1. Pegar una URL real.
2. Capturar HTML.
3. Extraer datos estructurados con Anthropic.
4. Identificar el set contra catalogo local.
5. Obtener fair price manual.
6. Calcular margen bruto, margen neto y score.
7. Guardar el resultado en SQLite.
8. Ver ultimos analisis.
9. Abrir detalle de analisis guardado.
10. Mostrar una experiencia visual premium en Streamlit.

## Limitaciones actuales

Estas limitaciones son conocidas y no se consideran bugs de V1:

- catalogo local pequeno
- fair prices manuales
- parser HTML basico
- marketplaces pueden bloquear o cambiar HTML
- eBay puede devolver 403
- no hay scraping masivo
- no hay precios en tiempo real
- SQLite local no es persistencia cloud robusta
- score es una senal explicable, no consejo financiero

## Material de portfolio

PDF final:

```text
docs/case_study/lego_resale_intelligence_case_study.pdf
```

Paginas para Behance:

```text
docs/case_study/preview/
```

Capturas de app:

```text
docs/screenshots/
```

## Decision de producto

La V1 no busca ser un producto comercial completo. Busca demostrar:

- pensamiento end-to-end
- criterio de arquitectura simple
- integracion LLM real
- modelado de datos
- scoring explicable
- persistencia
- testing
- UI premium dentro de una herramienta sencilla
- documentacion presentable para portfolio

## Punto de partida recomendado para V2

No empezar V2 con una gran reescritura.

La V2 deberia elegir una direccion clara entre estas opciones:

1. **Mejorar inteligencia de mercado**
   - ampliar catalogo
   - mejorar referencias de precio
   - historico de precios
   - comparables por set

2. **Mejorar robustez tecnica**
   - errores mas especificos por marketplace
   - parser mas estable
   - fallback manual cuando falle la captura
   - logs estructurados

3. **Mejorar utilidad de producto**
   - watchlist
   - estado del listing
   - decision final: comprar / vigilar / descartar
   - notas manuales del usuario

4. **Preparar deploy serio**
   - secrets en Streamlit Cloud
   - persistencia remota
   - demo dataset reproducible
   - limpieza de datos locales

Recomendacion: para V2, empezar por **ampliar catalogo + mejorar fallback manual + watchlist simple**, sin tocar todavia la arquitectura completa.

## Prompt recomendado para iniciar otro chat

```text
Estoy continuando el proyecto LEGO Resale Intelligence.

Ya existe una V1 terminada y documentada. Lee primero:
- docs/project_summary.md
- README.md

Contexto:
- App Python/Streamlit con Anthropic, SQLite, SQLAlchemy, Pydantic, BeautifulSoup y pytest.
- V1 ya tiene capture, extract, identify, pricing_reference, scoring, db, pipeline y UI premium.
- No quiero reescribir la app.
- Quiero empezar V2 de forma incremental, manteniendo claridad y evitando sobreingenieria.
- Prioriza codigo simple, legible y explicaciones en espanol.

Antes de proponer cambios:
1. Revisa el estado actual.
2. Dime que parte de V2 conviene atacar primero.
3. Propón un bloque pequeno, implementable y testeable.
```

