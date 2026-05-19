# V2 guide gap analysis

Avance demo local: **97/100**

Avance contra la guia completa: **84/100**

Este documento separa dos cosas que se estaban mezclando:

- **Demo local V2**: ya es una app navegable, defendible y ensenable.
- **Guia Maestra V2 completa**: pide una version mucho mas ambiciosa, publicada, con Postgres, mas datos, briefings Sonnet y material final de portfolio.

## Lectura honesta

La V2 actual no esta al principio. Tiene backend, frontend, datos seed, watchlist, set intelligence, portfolio, briefings locales y flujo demo sin coste.

Pero la guia completa no era solo "hacer una app local bonita". La guia apuntaba a:

- arquitectura cloud;
- PostgreSQL;
- datos ampliados;
- API publica;
- frontend publicado;
- briefings IA reales;
- artefactos finales de portfolio.

Por eso desde ahora usaremos dos porcentajes:

```text
Demo local: 94/100
Guia completa: 76/100
```

## Matriz de cumplimiento

| Area de la guia | Estado | Comentario |
|---|---:|---|
| FastAPI backend | Completo | API local con routers principales y docs FastAPI. |
| Next.js frontend | Completo local | Web navegable con Market, Analyze, Watchlist, Sets, Portfolio y Briefings. |
| Reutilizar V1 | Completo | `POST /api/analyze` usa el pipeline V1. |
| Demo sin coste | Completo | `POST /api/analyze/demo` evita Anthropic y marketplaces. |
| Watchlist | Parcial-alto | Funciona con SQLite compartida; falta modelo cloud dedicado. |
| Pricing dinamico | Parcial-alto | Motor existe; 50 snapshots para 10 sets activos; falta BrickLink guide curado grande hacia 300 sets. |
| Set Intelligence | Parcial-alto | Fair price, tendencia y chart; falta ficha profunda por set/categoria. |
| Portfolio P&L | Parcial-alto | CRUD completo: POST/DELETE + AddPositionPanel; falta persistencia cloud y transacciones. |
| Briefings IA | Parcial-alto | Claude Sonnet conectado con fallback local; falta persistencia DB y briefing semanal. |
| PostgreSQL | Parcial | Capa DB preparada con URL Postgres; falta instancia real local/cloud. |
| Alembic | Parcial-alto | Configuracion y migracion inicial creadas y verificadas en SQLite local. |
| Catalogo 300+ sets | Pendiente | Hay quality gate, 40 candidatos, UI de madurez, Research filtrable y checklist de promoción; seguimos con catálogo activo pequeño y seed data. |
| BrickLink data | Pendiente | No hay ingesta/curado amplio de BrickLink price guide. |
| UI 2D premium | Completo | Rediseno completo sin 3D: stat-strip, page-header, trend-badge, AddPositionPanel. |
| Tailwind/shadcn | No aplicado literalmente | Se uso CSS propio premium; visualmente cumple, stack exacto no. |
| Deploy backend | Pendiente | API local, no Railway/Render aun. |
| Deploy frontend | Pendiente | Web local, no Vercel aun. |
| API publica | Pendiente | `/docs` existe local, no publica. |
| Capturas V2 | Pendiente | Falta generar capturas desktop/mobile. |
| Video demo | Pendiente | Falta Loom/video. |
| Case study V2 | Pendiente | Hay story, falta PDF/case visual final. |

## Lo que queda para seguir la guia

### Bloque 1 - Base de datos profesional

Objetivo:

- introducir PostgreSQL;
- anadir Alembic;
- separar modelo local demo de modelo persistente;
- definir tablas reales para `price_history`, `portfolio_items`, `transactions`, `market_briefings` y `watchlist`.

Dependencia manual probable:

- instalar o usar Postgres local;
- o crear Postgres en Railway cuando toque deploy.

### Bloque 2 - Datos reales/curados

Objetivo:

- ampliar catalogo primero a 50 sets;
- luego ir hacia 300+;
- crear JSON/CSV curado de BrickLink price guide;
- tener al menos 5 snapshots por set activo antes de confiar en pricing.

### Bloque 3 - Portfolio editable

Objetivo:

- crear UI para anadir compra;
- registrar coste, cantidad, fecha, estado y target;
- anadir ventas/transacciones;
- calcular P&L realizado y no realizado.

### Bloque 4 - Briefings Sonnet

Objetivo:

- activar Claude Sonnet para briefing;
- controlar coste con limites;
- guardar token count;
- fallback si Sonnet falla;
- generar briefing on-demand y luego semanal.

### Bloque 5 - Deploy real

Objetivo:

- backend en Railway/Render;
- frontend en Vercel;
- `NEXT_PUBLIC_API_URL` apuntando al backend;
- API docs publica;
- variables de entorno seguras.

### Bloque 6 - Portfolio final

Objetivo:

- capturas desktop/mobile;
- diagrama arquitectura V2;
- case study PDF V2;
- video demo;
- README final con links publicos.

## Proxima fase recomendada

Si queremos seguir la guia de verdad, la siguiente fase debe ser:

**Fase G4 - Data expansion to 50 curated sets**

Por que:

- pricing y portfolio ya leen desde DB V2;
- el siguiente salto de valor es aumentar cobertura;
- primero 50 sets curados antes de intentar 300+;
- el pricing sera mas creible si hay mas historico por set.

Antes de tocar codigo, conviene decidir:

1. Validar manualmente los 40 candidatos de `data/catalog_expansion_candidates.csv`.
2. Promover candidatos validados a `data/catalog.csv`.
3. Ampliar `data/price_history_seed.json` con snapshots suficientes.
4. Ejecutar `scripts/v2_check_candidate_readiness.py` para bloquear candidatos sin evidencias.
5. Ejecutar `scripts/v2_validate_seed_data.py` antes de cargar datos.
6. Ejecutar `scripts/v2_seed_db.py` para cargar la DB V2.
