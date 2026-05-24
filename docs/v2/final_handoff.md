# LEGO Resale Intelligence V2 - Final handoff

Avance demo local: **99/100**

Avance contra la guia completa: **90/100**

## Estado real

La V2 esta lista como demo local avanzada, proyecto de portfolio ensenable y demo publica Railway/Vercel.

No es todavia una plataforma publica de datos verificados en tiempo real. El catalogo activo tiene 50 sets, un sistema de calidad de datos, y una primera tanda de auditoria real con 20 sets revisados.

## Que esta hecho

- V1 Streamlit se mantiene viva como producto legacy.
- V2 vive en el mismo repo, sin reescribir la app original.
- Backend FastAPI funcionando.
- Frontend Next.js funcionando.
- UI premium 2D inspirada en Linear/Stripe, sin 3D.
- Rutas V2 principales: Market, Analyze, Sets, Watchlist, Research, Portfolio, Briefings.
- Pricing seed dinamico.
- Historico seed de precios para 50 sets.
- Portfolio con P&L y CRUD basico.
- Watchlist compartida con SQLite V1.
- Briefings con integracion Claude y fallback local.
- Sistema de data quality.
- Endpoint y UI de madurez de datos.
- Auditoria activa de evidencias.
- Preparacion para Railway/Vercel.
- Manual simple de publicacion.
- Case study V2 en Markdown y HTML.

## Validacion local

Ultima validacion local conocida:

- `pytest`: 116 passed.
- `npm run build`: OK.
- `bash scripts/v2_doctor.sh`: OK.
- `scripts/v2_deploy_smoke.sh` contra localhost: OK.

URLs locales:

- Web V2: `http://127.0.0.1:3000`
- API docs: `http://127.0.0.1:8000/docs`

## Como explicarlo en portfolio

Frase recomendada:

> Seed-backed LEGO resale intelligence prototype with production-style architecture, data-quality gates and portfolio workflows.

Evitar decir:

> Verified live LEGO market pricing platform.

Porque el catalogo de 50 sets todavia no esta verificado con evidencias externas completas.

## Data status

Estado actual:

- `active_catalog_verified_sets`: 5
- `active_catalog_evidence_started_sets`: 20
- `active_catalog_blocked_sets`: 15
- `market_data_source_status`: `partially_verified`

Primeros sets auditados en FASE DATA-1:

- Verificados: `10221`, `75252`, `75313`, `75059`, `75095`.
- Bloqueados o en revision: 15 sets, incluyendo `75192`, `21309`, `10214`, `10179`, `10030`, `10212`, `75060`, `75144`, `75159`, `75275`, `75309`, `10182`, `10185`, `10197`, `10211`.

## Lo que falta para 100/100

1. Verificar los 30 sets restantes con evidencias reales.
2. Resolver discrepancias de `75192`, `21309`, `10214`, `10179` y `10030`.
3. Opcional: activar Railway Postgres y migraciones.
4. Mantener el smoke test publico despues de cada deploy.

## Archivos clave

- `README.md`
- `docs/v2/README.md`
- `docs/v2/publish_manual_for_juan.md`
- `docs/v2/deploy_plan.md`
- `docs/v2/release_checklist.md`
- `docs/v2/data_quality_notes.md`
- `docs/v2/final_handoff.md`
- `docs/case_study/lego_resale_intelligence_v2_case_study.md`
- `docs/case_study/lego_resale_intelligence_v2_case_study.html`
- `data/catalog_active_research.json`

## Siguiente decision

La siguiente decision no es de codigo, es de publicacion:

- seguir solo como portfolio local;
- o publicar en Railway/Vercel;
- o publicar con Postgres para persistencia cloud real.

Para portfolio, la opcion recomendada es publicar Railway + Vercel primero sin Postgres, validar que la demo publica funciona, y despues anadir Postgres si hace falta.
