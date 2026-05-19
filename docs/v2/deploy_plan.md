# V2 deploy plan

Avance demo local: **94/100**

Avance contra la guia completa: **76/100**

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

## Backend

Proveedor recomendado: Railway o Render.

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Variables:

```env
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
DATABASE_URL=
```

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
DATABASE_URL=postgresql+psycopg://...
```

Trabajo pendiente antes de Postgres:

- conectar una instancia Postgres real;
- ejecutar migraciones y seed sobre esa instancia;
- definir backups;
- decidir retention de watchlist y price history.

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

## Riesgos

- El extractor real depende de HTML externo.
- eBay/Wallapop pueden bloquear o cambiar estructuras.
- Los historicos actuales son seed data.
- La demo de briefing aun no llama a Claude.
- Persistencia cloud requiere Postgres o volumen persistente.

## Secuencia recomendada

1. Publicar backend con demo endpoints.
2. Verificar `/health` y `/docs`.
3. Publicar frontend con `NEXT_PUBLIC_API_URL`.
4. Verificar rutas principales.
5. Activar Anthropic solo cuando el flujo demo este estable.
6. Migrar SQLite a Postgres si la watchlist debe persistir en cloud.
