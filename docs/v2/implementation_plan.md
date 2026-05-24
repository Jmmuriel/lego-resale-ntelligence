# Plan de implementación V2

Avance demo local: **99/100**

Avance contra la guía completa: **90/100**

## Principio

La guía V2 propone un producto mucho más ambicioso que V1: pasar de analizar una URL a tener inteligencia de mercado, portfolio, pricing dinámico y briefings IA.

Lo vamos a hacer, pero de forma incremental:

- no rompemos V1;
- no empezamos por el frontend bonito;
- no migramos todo a la vez;
- cada fase debe poder probarse;
- cada decisión debe poder explicarse en entrevista.

Nota importante:

- el 99/100 mide la **demo local V2**;
- el 90/100 mide la **Guía Maestra V2 completa**;
- el seguimiento detallado de brechas vive en `docs/v2/guide_gap_analysis.md`.

## Fase 0A - Ordenar V2 dentro del repo

Estado: **completada**

Objetivo simple: dejar claro dónde vive V2 y cuál es el plan antes de tocar arquitectura.

Entregables:

- `docs/v2/lego_resale_intelligence_v2_guide.pdf`
- `docs/v2/README.md`
- `docs/v2/implementation_plan.md`
- decisión documentada: V1 y V2 viven en el mismo repo

Qué significa para alguien no técnico:

Estamos poniendo todos los planos de la reforma en una carpeta del proyecto. Todavía no estamos tirando paredes.

## Fase 0B - Backend mínimo

Estado: **completada**

Objetivo: crear una API FastAPI mínima que responda.

Entregables:

- `backend/main.py`
- endpoint `/health`
- estructura inicial de routers
- test mínimo que confirme que la API está viva

Qué significa:

Crear el motor nuevo, pero solo encenderlo y comprobar que arranca.

Resultado actual:

- `backend/main.py` creado;
- endpoint `/health` disponible;
- routers iniciales registrados con endpoints `/ping`;
- tests mínimos añadidos en `tests/test_backend_health.py`.

## Fase 1A - Reutilizar análisis V1 desde la API

Estado: **completada**

Objetivo: que FastAPI pueda llamar al pipeline actual de V1.

Entregables:

- endpoint `POST /api/analyze`
- respuesta JSON con el análisis actual
- tests con mocks

Qué significa:

La V2 empieza usando el cerebro que ya funciona en V1, en vez de reinventarlo.

Resultado actual:

- endpoint `POST /api/analyze` disponible;
- usa `src.pipeline.analyze_listing_url`;
- devuelve `ListingAnalysis` como JSON;
- convierte errores controlados del pipeline en respuesta HTTP 422;
- tests de API añadidos con mocks.

## Fase 1B - Decisión de base de datos

Estado: **completada**

Objetivo: decidir cuándo pasar de SQLite a PostgreSQL.

Opción recomendada:

- mantener SQLite mientras la API se estabiliza;
- introducir PostgreSQL + Alembic cuando vayamos a `price_history`, `portfolio_items` y `market_briefings`.

Qué significa:

No cambiamos el suelo de la casa mientras todavía estamos comprobando dónde van las habitaciones.

Resultado actual:

- decisión documentada en `docs/v2/database_decision.md`;
- se mantiene SQLite para el tramo inicial;
- PostgreSQL + Alembic quedan reservados para cuando existan tablas temporales y financieras reales.

## Fase 2A - Pricing dinámico pequeño

Estado: **completada**

Objetivo: crear el motor de precios dinámicos con pocos sets primero.

Entregables:

- modelo `PriceHistory`
- datos seed para 10-20 sets, no 300 al principio
- cálculo de fair price desde histórico
- anomaly score

Qué significa:

Primero demostramos que el sistema entiende precios en el tiempo. Luego ya ampliamos volumen.

Resultado actual:

- histórico seed en `data/price_history_seed.json`;
- motor en `backend/services/price_engine.py`;
- endpoint `GET /api/market/price/{set_id}`;
- endpoint `GET /api/market/trends`;
- tests de fair price, confianza, anomalía y tendencias.

## Fase 2B - Conectar pricing dinámico al análisis

Estado: **completada**

Objetivo: enriquecer el resultado de `POST /api/analyze` con contexto de mercado V2.

Entregables:

- `anomaly_score`;
- fair price dinámico cuando haya histórico;
- fallback al precio manual de V1 cuando no haya datos;
- tests que prueben ambos caminos.

Qué significa:

El análisis de una URL ya no solo dirá si hay margen. También podrá decir si el precio está raro frente al mercado reciente.

Resultado actual:

- `POST /api/analyze` devuelve `market_context`;
- `market_context` incluye fair price usado, fuente, confianza y `anomaly_score`;
- usa histórico dinámico cuando existe;
- cae a precio manual de V1 cuando no hay histórico;
- V1 de Streamlit no cambia.

## Fase 4A - Portfolio mínimo

Estado: **completada**

Objetivo: registrar compras y calcular P&L básico.

Entregables:

- posiciones de portfolio;
- coste de compra;
- valor actual estimado;
- P&L no realizado;
- señal simple `HOLD`, `NEUTRAL` o `SELL`.

Qué significa:

El sistema ya no solo dice si comprar algo; también entiende lo que ya tienes.

Resultado actual:

- seed de portfolio en `data/portfolio_seed.json`;
- motor financiero en `backend/services/portfolio_engine.py`;
- endpoint `GET /api/portfolio`;
- endpoint `GET /api/portfolio/positions`;
- cálculo de P&L no realizado y señal `HOLD`, `NEUTRAL`, `SELL`.

## Fase 3A - Briefing IA mínimo

Estado: **completada**

Objetivo: generar un briefing útil con datos reales del sistema.

Entregables:

- prompt fijo para Claude Sonnet;
- endpoint para generar briefing;
- guardado del briefing;
- test con respuesta mock.

Qué significa:

La IA deja de extraer texto solamente y empieza a resumir qué está pasando en el mercado.

Resultado actual:

- briefing local en `backend/services/ai_analyst.py`;
- endpoint `GET /api/briefings`;
- endpoint `POST /api/briefings/generate`;
- `used_llm=false` y `token_count=0` para evitar gasto de API;
- system prompt documentado para futura conexión con Claude Sonnet.

## Fase 5 - Frontend Next.js

Estado: **funcionando en local**

Objetivo: construir la web V2 cuando ya haya datos reales detrás.

Primera versión razonable:

- Market Overview;
- Analyze;
- Portfolio.

Después:

- Set Intelligence;
- Briefings;
- Opportunity Scanner completo.

Qué significa:

No hacemos una fachada bonita vacía. Primero motor, luego pantalla.

Resultado actual:

- dirección visual documentada en `docs/v2/ui_direction.md`;
- inspiración principal: Linear + Stripe;
- LEGO adulto integrado como acento visual;
- 3D propuesto de forma sobria para Market Overview.
- scaffold inicial en `frontend/`;
- Market Overview inicial diseñado con layout Collector Terminal;
- cliente API tipado en `frontend/src/lib/api.ts`;
- tipos TypeScript alineados con la API actual.
- dependencias instaladas con npm;
- `npm run build` completado correctamente;
- backend y frontend levantan en local;
- navegación V2 real con `Market`, `Analyze`, `Sets`, `Portfolio` y `Briefings`;
- escena Three.js inicial en Market Overview;
- endpoint `GET /api/market/set/{set_id}`;
- endpoint `GET /api/market/history/{set_id}`;
- pantalla `Sets` con fair price, confianza, tendencia y resumen de mercado;
- gráfico de histórico de precio medio en `Sets`;
- endpoints V2 de watchlist para listar, guardar y cambiar estado;
- endpoint `POST /api/analyze/demo` para demo sin coste de Anthropic;
- botón `Save to watchlist` en `Analyze`;
- pantalla `Watchlist` con filtros por estado y acciones de workflow;
- ciclo operativo completo `Analyze -> Save -> Watchlist -> Status`;
- runbook de demo en `docs/v2/demo_runbook.md`;
- checklist de publicacion en `docs/v2/release_checklist.md`;
- scripts de arranque `scripts/v2_start_api.sh` y `scripts/v2_start_frontend.sh`;
- doctor de rutas `scripts/v2_doctor.sh`;
- variables frontend documentadas en `frontend/.env.example`;
- narrativa de portfolio en `docs/v2/portfolio_story.md`;
- plan de deploy en `docs/v2/deploy_plan.md`;
- `.gitignore` actualizado para excluir `frontend/node_modules/`, `frontend/.next/` y secretos locales.

## Fase UI-2D - Rediseño premium sin 3D

Estado: **completada**

Objetivo: rediseñar completamente la UI eliminando Three.js y adoptando un terminal 2D premium (Linear + Stripe).

Entregables:

- eliminación de `BrickSignalScene.tsx` y dependencias Three.js;
- nuevo sistema de diseño CSS completo (stat-strip, page-header, btn-primary/btn-ghost, trend-badge, inline-form);
- `SidebarNav` con 7 iconos SVG inline;
- Market Overview con stat-strip de 5 métricas y content-grid sin hero 3D;
- todas las páginas con `page-header` compacto, sin texto tutorial;
- `AddPositionPanel` con form completo de portfolio CRUD;
- `npm run build` compilando correctamente.

## Fase Backend-G5 - Sonnet + Portfolio CRUD + Price history expansion

Estado: **completada**

Objetivo: conectar Claude Sonnet real, añadir CRUD de portfolio y expandir datos de precios.

Entregables:

- `generate_briefing_with_llm()` en `ai_analyst.py` con fallback local;
- `POST /api/briefings/generate?use_llm=true` usa Sonnet si hay API key;
- `POST /api/portfolio` y `DELETE /api/portfolio/{id}`;
- `add_portfolio_item()` y `delete_portfolio_item()` en `portfolio_engine.py`;
- `data/price_history_seed.json` expandido a 250 snapshots (5 por set, 50 sets activos);
- tests actualizados: 114 pasando.

## Fase 6 - Publicación y portfolio

Objetivo: dejar V2 enseñable.

Entregables:

- README V2;
- capturas;
- demo;
- API docs públicas;
- case study V2;
- narrativa V1 -> V2.

## Fase G1 - PostgreSQL + Alembic foundation

Estado: **completada parcialmente**

Objetivo: empezar a cumplir la guía completa, no solo la demo local.

Entregables:

- dependencias para Postgres/Alembic;
- estructura `backend/db/`;
- modelos SQLAlchemy V2 para tablas nuevas;
- migración inicial;
- decisión clara de compatibilidad con SQLite demo.

Qué significa:

Hasta ahora tenemos una demo local fuerte. Esta fase empieza a convertirla en arquitectura publicable y persistente.

Resultado actual:

- `alembic` y `psycopg[binary]` añadidos a `requirements.txt`;
- `backend/db/database.py` creado;
- `backend/db/models.py` creado con tablas de la guia;
- `backend/db/crud.py` creado con CRUD inicial de catalogo;
- `alembic.ini` y carpeta de migraciones añadidas;
- migracion inicial `20260517_0001_initial_v2_schema.py`;
- `.venv/bin/alembic upgrade head` verificado contra SQLite local;
- tests V2 DB añadidos;
- suite completa: 99 tests pasando.

## Fase G2 - Seed data migration

Estado: **completada**

Objetivo: mover los datos seed actuales a la nueva base V2.

Entregables:

- script de carga de `data/price_history_seed.json`;
- script de carga de `data/portfolio_seed.json`;
- tests de carga idempotente;
- servicios con fallback DB -> JSON o migracion directa a DB.

Resultado actual:

- `scripts/v2_seed_db.py` creado;
- carga catalogo, price history y portfolio;
- carga idempotente verificada;
- `tests/test_v2_seed_db.py` añadido;
- `.venv/bin/python scripts/v2_seed_db.py` ejecutado correctamente;
- suite completa tras G2: 101 tests pasando.

## Fase G3 - Services read from DB with JSON fallback

Estado: **completada**

Objetivo: hacer que pricing y portfolio usen DB V2 cuando exista data cargada.

Entregables:

- lectura DB en `price_engine`;
- lectura DB en `portfolio_engine`;
- fallback JSON si no hay DB o no hay datos;
- tests para ambos caminos.

Resultado actual:

- `price_engine` intenta leer `price_history` desde DB V2 primero;
- `portfolio_engine` intenta leer `portfolio_items` desde DB V2 primero;
- si la DB no existe, no tiene tablas o está vacía, se conserva fallback JSON;
- tests añadidos para carga desde SQLite temporal y preferencia DB;
- suite completa: 105 tests pasando.

## Fase G4A - Seed data quality gate

Estado: **completada**

Objetivo: preparar el crecimiento hacia 50 sets sin romper consistencia de datos.

Entregables:

- script de validación para `data/catalog.csv`;
- script de validación para `data/price_history_seed.json`;
- script de validación para `data/portfolio_seed.json`;
- métricas de cobertura frente al objetivo de 50 sets;
- tests de datos válidos y datos inválidos.

Resultado actual:

- `scripts/v2_validate_seed_data.py` creado;
- detecta sets duplicados, referencias a sets inexistentes, bandas de precio inválidas y campos mal formateados;
- valida que el catálogo seed actual llega a 50/50 sets;
- deja `data/catalog_expansion_candidates.csv` preparado para futuros candidatos;
- expone `GET /api/market/data-quality`;
- expone `GET /api/market/catalog-candidates`;
- muestra madurez de datos en Market Overview;
- añade página `Research` para revisar futuros candidatos sin activarlos;
- añade búsqueda y filtro por tema en la cola Research;
- añade un checklist de 8 evidencias por candidato antes de poder promocionarlo;
- expone `candidate_ready_for_promotion` en la API de madurez de datos;
- añade `scripts/v2_check_candidate_readiness.py` como candado previo a la promoción;
- `setup.sh` recomienda validar antes de cargar seed en DB;
- suite completa: 114 tests pasando.

## Métrica de avance

Para la demo local usamos una escala simple sobre 100:

- 0-10: planificación y estructura;
- 10-25: backend mínimo y análisis heredado;
- 25-45: pricing dinámico y datos históricos;
- 45-60: portfolio y briefings IA;
- 60-80: frontend Next.js;
- 80-95: deploy, seed data y polish;
- 95-100: documentación final y portfolio público.

Para la guía completa, el avance actual es 90/100 porque ya existe foundation PostgreSQL/Alembic, carga seed a DB V2, servicios leyendo DB con fallback JSON, validación automática de seed data, catálogo seed de 50 sets, 250 snapshots, UI 2D premium, portfolio CRUD básico, Sonnet con fallback local, superficie API/UI de madurez de datos, auditoría activa de evidencias, preparación Railway/Vercel y case study V2. Falta publicar con cuentas reales, conectar Postgres cloud real y ampliar evidencia verificada por set.
