# DB read fallback notes

Avance demo local: **99/100**

Avance contra la guia completa: **90/100**

## Qué se ha hecho

Pricing y portfolio ya leen desde la base de datos V2 cuando hay datos cargados.

Si la base de datos no existe, no tiene tablas o está vacía, la app vuelve a usar los archivos JSON seed. Esto mantiene la demo local estable mientras avanzamos hacia Postgres real.

## Por qué mejora la V2

Antes:

- `price_engine` leía solo `data/price_history_seed.json`;
- `portfolio_engine` leía solo `data/portfolio_seed.json`;
- la DB V2 existía, pero los servicios principales aún no la usaban.

Ahora:

- `price_engine` intenta leer `price_history` desde DB V2 primero;
- `portfolio_engine` intenta leer `portfolio_items` desde DB V2 primero;
- los tests prueban SQLite temporal y preferencia DB;
- el fallback JSON evita romper desarrollo local.

## En sencillo

Es como cambiar de una libreta provisional a una base de datos, pero dejando la libreta guardada por si la base aún no está encendida.

## Verificación

```bash
.venv/bin/pytest
```

Resultado:

```text
114 passed
```

## Siguiente paso recomendado

**G5 - Evidence-backed data expansion**

El sistema ya sabe dónde leer los datos y la seed local llega a 50 sets. Ahora toca añadir evidencia/fuentes trazables y escalar con cuidado hacia 300+.
