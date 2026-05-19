# Decisión de base de datos V2

Avance V2: **18/100**

Fecha: 2026-05-14

## Decisión

V2 no migrará inmediatamente a PostgreSQL.

La decisión actual es:

- mantener SQLite durante la conexión inicial de FastAPI con el pipeline de V1;
- introducir PostgreSQL + Alembic cuando empiece la capa temporal real:
  - `price_history`;
  - `portfolio_items`;
  - `transactions`;
  - `market_briefings`;
  - `watchlist` persistente V2.

## Por qué

SQLite ya funciona en V1 y está cubierto por tests. Para los primeros pasos de V2, el objetivo no es demostrar una base de datos nueva, sino demostrar que la API puede reutilizar el análisis existente.

Cambiar a PostgreSQL antes de tener datos temporales reales añadiría complejidad sin mejorar todavía el producto.

## Qué significa en sencillo

No vamos a cambiar el almacén principal justo al empezar la reforma.

Primero conectamos la API nueva con el motor que ya funciona. Cuando el producto necesite guardar historial de precios, portfolio y briefings, entonces sí usaremos PostgreSQL porque ahí empieza a aportar valor real.

## Cuándo cambiaremos a PostgreSQL

El cambio se activa al empezar Fase 2A o Fase 4A, según cuál necesite persistencia nueva primero.

La señal clara será:

- necesitamos guardar muchas observaciones por set y fecha;
- necesitamos relaciones entre portfolio, transacciones y listings;
- necesitamos migraciones versionadas para evolucionar tablas sin borrar datos.

## Qué se mantiene por ahora

- `src/db.py` sigue siendo la persistencia V1.
- `DATABASE_URL` sigue aceptando SQLite.
- FastAPI puede usar el pipeline V1 sin conocer aún los detalles de PostgreSQL.

## Riesgo aceptado

Durante este tramo, la API V2 todavía depende de la persistencia V1.

Esto es aceptable porque el objetivo de esta fase es integración incremental, no arquitectura final.

## Cómo lo explicamos en portfolio

La migración a PostgreSQL no se hizo por moda. Se pospuso hasta que el modelo de datos necesitó historial temporal, relaciones financieras y migraciones versionadas.
