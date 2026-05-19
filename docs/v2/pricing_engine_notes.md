# Pricing engine V2

Avance V2: **32/100**

Fecha: 2026-05-14

## Estado

Fase 2A implementada como primera versión pequeña.

El sistema ya puede calcular un fair price dinámico usando histórico curado. Ahora intenta leer primero desde la DB V2 y conserva JSON como respaldo local.

## Qué se añadió

- `data/price_history_seed.json`
- `backend/services/price_engine.py`
- endpoint `GET /api/market/price/{set_id}`
- endpoint `GET /api/market/trends`
- enriquecimiento de `POST /api/analyze` con `market_context`
- lectura de `price_history` desde DB V2 con fallback JSON
- tests en `tests/test_price_engine.py`

## Qué significa en sencillo

Antes, el sistema miraba un precio fijo escrito a mano.

Ahora mira varias observaciones de precio en distintas fechas y calcula un precio justo ponderando más los datos recientes.

## Qué datos cubre esta primera versión

Es una semilla pequeña, no una base completa:

- `75192` Millennium Falcon UCS
- `75313` AT-AT UCS
- `75095` TIE Fighter UCS
- `10214` Tower Bridge

## Qué devuelve el motor

Para un set y condición, devuelve:

- precio medio dinámico;
- mínimo observado;
- máximo observado;
- confianza (`HIGH`, `MEDIUM`, `LOW`, `NONE`);
- número de snapshots usados;
- días desde la última actualización.

También calcula `anomaly_score`:

- negativo = el listing está barato respecto al mercado;
- positivo = el listing está caro respecto al mercado.

## Qué NO es todavía

No es aún el sistema final de pricing de la guía.

Falta:

- ampliar a más sets;
- añadir contexto de mercado completo al resultado del listing;
- conectar una instancia PostgreSQL real cuando toque deploy;
- cargar un histórico BrickLink más amplio y validado.

## Decisión consciente

Se implementó primero con JSON seed porque permite validar la lógica sin añadir una migración de base de datos demasiado pronto.

Ahora el código ya soporta el salto: DB V2 primero, JSON si la DB no está lista. Cuando tengamos Postgres real, el mismo camino servirá para publicar sin cambiar la lógica principal.
