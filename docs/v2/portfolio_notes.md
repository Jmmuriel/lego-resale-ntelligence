# Portfolio mínimo V2

Avance V2: **43/100**

Fecha: 2026-05-14

## Estado

Portfolio mínimo implementado con datos seed. Ahora intenta leer primero desde la DB V2 y conserva JSON como respaldo local.

Esta fase se adelantó antes del briefing IA porque el portfolio genera datos útiles para que los briefings posteriores tengan más sustancia.

## Qué se añadió

- `data/portfolio_seed.json`
- `backend/services/portfolio_engine.py`
- endpoint `GET /api/portfolio`
- endpoint `GET /api/portfolio/positions`
- lectura de `portfolio_items` desde DB V2 con fallback JSON
- tests en `tests/test_portfolio_engine.py`

## Qué significa en sencillo

El sistema ya puede leer una lista de sets comprados, estimar cuánto valen hoy, restar comisiones/envío de salida y calcular si la posición va ganando o perdiendo.

## Qué calcula

Por cada posición:

- coste de compra;
- valor fair price actual;
- neto estimado si se vendiera hoy;
- P&L no realizado en euros;
- P&L no realizado en porcentaje;
- días en cartera;
- confianza del precio;
- señal `HOLD`, `NEUTRAL` o `SELL`;
- razón breve de la señal.

En resumen:

- coste total;
- valor actual estimado;
- neto si se vendiera todo;
- P&L total;
- posición mejor;
- posición peor;
- señal dominante.

## Qué NO es todavía

No es aún un portfolio editable completo.

Falta:

- formulario/API para añadir posiciones manualmente;
- registrar ventas;
- calcular P&L realizado;
- conectar una instancia PostgreSQL real cuando toque persistencia seria;
- usar tus compras reales si quieres que sea 100% creíble para portfolio público.

## Decisión consciente

Se empezó con JSON seed para validar la lógica financiera sin pedir todavía datos personales ni migrar base de datos.

Ahora el portfolio seed ya puede vivir en DB V2. El siguiente paso de producto es crear alta/edición de posiciones desde la web.
