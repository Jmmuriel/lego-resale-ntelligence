# PostgreSQL + Alembic foundation

Avance demo local: **94/100**

Avance contra la guia completa: **76/100**

Esta fase inicia la parte de base de datos profesional que pide la guia completa.

## Qué se añadió

- Dependencias:
  - `alembic`
  - `psycopg[binary]`
- Configuracion Alembic:
  - `alembic.ini`
  - `backend/db/migrations/env.py`
  - `backend/db/migrations/script.py.mako`
  - primera migracion en `backend/db/migrations/versions/`
- Capa DB V2:
  - `backend/db/database.py`
  - `backend/db/models.py`
  - `backend/db/crud.py`

## Tablas V2 preparadas

- `set_catalog`
- `price_history`
- `listings`
- `portfolio_items`
- `transactions`
- `market_briefings`

## Por qué mejora la app

Antes:

- SQLite local servia para demo;
- los datos V2 vivian solo en JSON seed;
- no habia historial formal de cambios de esquema;
- publicar con persistencia real era dificil.

Ahora:

- existe un esquema V2 formal;
- existe migracion inicial auditable;
- se puede usar SQLite para demo local o Postgres para deploy;
- pricing, portfolio, listings y briefings ya tienen tablas destino;
- pricing y portfolio ya pueden leer desde DB V2 con fallback JSON;
- la arquitectura se acerca a la guia completa.

## Variables

Para demo local:

```env
V2_DATABASE_URL=sqlite:///db/lri_v2.db
```

Para Postgres futuro:

```env
V2_DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname
```

Si `V2_DATABASE_URL` no existe, se usa `DATABASE_URL`, y si tampoco existe, SQLite local.

## Comandos

Ejecutar migracion:

```bash
.venv/bin/alembic upgrade head
```

Ejecutar tests:

```bash
.venv/bin/pytest
```

Resultado actual:

```text
114 passed
```

## Qué no hace todavía

- No conecta todavía watchlist, listings ni briefings a estas tablas V2.
- No levanta Postgres local ni cloud.
- No sustituye la SQLite legacy de V1.

Esto es intencional: la base profesional queda lista sin romper la demo que ya funciona.

## Siguiente paso recomendado

**G2 - Seed data migration**

Mover los JSON actuales (`price_history_seed.json` y `portfolio_seed.json`) a scripts de carga sobre la nueva base V2.

Estado: **completado**

Resultado:

- `scripts/v2_seed_db.py`;
- carga `data/catalog.csv`;
- carga `data/price_history_seed.json`;
- carga `data/portfolio_seed.json`;
- es idempotente: puede ejecutarse varias veces sin duplicar datos;
- tests en `tests/test_v2_seed_db.py`;
- suite actual: `114 passed`.

## G3 - Lectura DB con fallback JSON

Estado: **completado**

Resultado:

- `backend/services/price_engine.py` lee `price_history` desde DB V2 primero;
- `backend/services/portfolio_engine.py` lee `portfolio_items` desde DB V2 primero;
- si la DB no está disponible o no tiene datos, se mantiene JSON seed;
- tests de lectura DB y preferencia DB añadidos;
- suite actual: `114 passed`.
