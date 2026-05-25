# V2 deploy plan

Avance demo local: **99/100**

Avance contra la guia completa: **90/100**

Plan recomendado para publicar LEGO Resale Intelligence V2.

## Decision recomendada

Publicar V2 como dos servicios:

- frontend en Vercel;
- backend en Railway o Render;
- base de datos Postgres cuando se quiera persistencia real.

Para demo local, SQLite sigue siendo suficiente.

## Por que no Streamlit Cloud para V2

Streamlit Cloud encaja con V1, pero V2 ya tiene:

- frontend Next.js;
- backend FastAPI;
- API separada;
- rutas frontend;
- posible Postgres;
- futura integracion de jobs/briefings.

Por eso V2 debe desplegarse como web + API.

## Frontend

Proveedor recomendado: Vercel.

Directorio:

```text
frontend/
```

Build command:

```bash
npm run build
```

Output:

```text
.next
```

Variable:

```env
NEXT_PUBLIC_API_URL=https://your-api-domain.example.com
```

Si se importa el repo completo en Vercel, configurar **Root Directory** como:

```text
frontend
```

## Backend

Proveedor recomendado: Railway o Render.

Railway ya puede usar el `Dockerfile` del repo.

Start command interno:

```bash
sh scripts/v2_boot_api.sh
```

Variables:

```env
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
DATABASE_URL=
V2_DATABASE_URL=
BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app
V2_RUN_MIGRATIONS=0
V2_SEED_DATABASE=0
```

Para Railway con Postgres:

```env
V2_DATABASE_URL=postgresql+psycopg://...
V2_RUN_MIGRATIONS=1
V2_SEED_DATABASE=1
```

Después del primer seed, cambiar `V2_SEED_DATABASE=0` para no sobrescribir datos editables en cada redeploy.

Para demo sin Anthropic:

- `POST /api/analyze/demo` funciona sin API key;
- Market, Sets, Portfolio, Watchlist y Briefings locales no gastan tokens.

## Base de datos

### Demo local

SQLite:

```env
DATABASE_URL=
```

La app usa:

```text
sqlite:///db/lri.db
```

### Deploy serio

Postgres:

```env
V2_DATABASE_URL=postgresql+psycopg://...
```

Trabajo pendiente antes de Postgres:

- conectar una instancia Postgres real;
- ejecutar migraciones y seed sobre esa instancia;
- definir backups;
- decidir retention de watchlist y price history.

El repo ya incluye:

- `scripts/v2_boot_api.sh` para arrancar Railway con migraciones/seed opcionales;
- `scripts/v2_deploy_smoke.sh` para comprobar API y web publicadas;
- `.dockerignore` para no subir `.env`, `.venv`, `node_modules`, `.next` ni bases locales al build Docker.

## Seguridad

No subir:

- `.env`;
- `db/*.db`;
- `frontend/.env.local`;
- `frontend/.next`;
- `frontend/node_modules`;
- claves Anthropic.

## Checklist previa

```bash
.venv/bin/pytest
cd frontend
npm run build
cd ..
bash scripts/v2_doctor.sh
```

Cuando existan URLs publicas:

```bash
API_URL=https://your-railway-api.up.railway.app \
WEB_URL=https://your-vercel-app.vercel.app \
sh scripts/v2_deploy_smoke.sh
```

## Riesgos

- El extractor real depende de HTML externo.
- eBay/Wallapop pueden bloquear o cambiar estructuras.
- Los historicos actuales son seed data.
- La demo de briefing aun no llama a Claude.
- Persistencia cloud requiere Postgres o volumen persistente.

## Secuencia recomendada

1. Publicar backend en Railway con `Dockerfile`.
2. Verificar `/health` y `/docs`.
3. Si se quiere persistencia, crear Postgres en Railway y usar `V2_DATABASE_URL`.
4. Ejecutar primer deploy con `V2_RUN_MIGRATIONS=1` y `V2_SEED_DATABASE=1`.
5. Cambiar `V2_SEED_DATABASE=0` después del primer seed.
6. Publicar frontend en Vercel con Root Directory `frontend`.
7. Configurar `NEXT_PUBLIC_API_URL` en Vercel apuntando al backend.
8. Configurar `BACKEND_CORS_ORIGINS` en Railway apuntando al dominio Vercel.
9. Ejecutar `scripts/v2_deploy_smoke.sh`.
10. Activar Anthropic solo cuando el flujo demo este estable.

## Estado honesto antes de deploy

La app está lista para demo pública como **partially verified seed-backed prototype**.

No afirmar todavía que los 50 sets son datos reales verificados:

- `active_catalog_verified_sets: 10`;
- `active_catalog_evidence_started_sets: 50`;
- `active_catalog_blocked_sets: 40`;
- `market_data_source_status: partially_verified`;
- 40 sets no cuentan como verificados hasta resolver discrepancias de retirada, piezas o PVP.
