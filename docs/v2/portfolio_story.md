# V2 portfolio story

Avance actual: **94/100**

Este documento resume la historia de LEGO Resale Intelligence para portfolio, entrevistas o case study.

## One-liner

LEGO Resale Intelligence convierte listings de sets descatalogados en senales de compra, watchlist, pricing dinamico seed, portfolio P&L y briefing de mercado.

## Problema

Comprar LEGO descatalogado para reventa exige revisar muchos factores a mano:

- precio pedido;
- coste de envio;
- estado del set;
- piezas/caja/instrucciones;
- fair price de mercado;
- margen despues de fees;
- riesgo de comprar caro o incompleto.

La decision no es solo "esta barato". Es una decision de margen, riesgo y timing.

## V1

La V1 resolvio el problema base con una app Streamlit:

- pega una URL real;
- descarga HTML;
- extrae datos estructurados con Anthropic;
- identifica el set contra catalogo local;
- calcula fair price manual, margen bruto, margen neto y score;
- guarda el resultado en SQLite;
- muestra una UI premium simple.

La V1 demostro que el pipeline funciona end-to-end.

## Limitacion de V1

V1 era util, pero seguia siendo una herramienta de analisis puntual:

- una URL cada vez;
- fair prices manuales;
- poca inteligencia temporal;
- portfolio separado del analisis;
- Streamlit limitaba la experiencia de producto;
- no habia vista clara de mercado, watchlist avanzada o set intelligence.

## V2

La V2 no reescribe V1. La convierte en el nucleo de una plataforma mas seria.

V2 introduce:

- API FastAPI;
- frontend Next.js;
- Market Overview;
- Analyze con pipeline V1 y contexto V2;
- demo opportunity sin coste de Anthropic;
- Watchlist compartida con SQLite;
- Set Intelligence con historico y fair price dinamico seed;
- Portfolio P&L;
- Briefings locales sin gasto de LLM;
- escena 3D premium con lenguaje LEGO adulto.

## Decisiones de producto

### Incremental, no rewrite

La V1 sigue viva. V2 reutiliza `src.pipeline`, `src.db` y los modelos existentes.

Esto evita tirar trabajo que ya funciona y demuestra criterio de ingenieria: evolucionar el producto sin romper la base.

### SQLite primero

SQLite se mantiene mientras la V2 valida flujos.

PostgreSQL queda para deploy serio con persistencia cloud, historicos reales y portfolio editable.

### Briefing local antes de LLM

El briefing actual es deterministico y no gasta tokens.

La integracion Claude Sonnet esta preparada conceptualmente, pero se pospone hasta que el flujo de producto este validado.

### Demo sin coste

`POST /api/analyze/demo` permite mostrar el flujo completo sin depender de marketplaces ni Anthropic.

Esto hace que la demo sea estable y barata.

## Demo flow

1. Abrir Market.
2. Mostrar dashboard y 3D brick.
3. Ir a Analyze.
4. Usar `Load no-cost demo opportunity`.
5. Guardar en watchlist.
6. Abrir Watchlist.
7. Cambiar estado.
8. Abrir Sets y probar `75192`.
9. Abrir Portfolio.
10. Abrir Briefings.

## Arquitectura V2

```text
Next.js frontend
  -> FastAPI backend
    -> V1 pipeline
    -> SQLite watchlist
    -> price history seed
    -> portfolio seed
    -> local briefing engine
```

## Resultado

V2 transforma una herramienta puntual en una experiencia de inteligencia de mercado:

- mas visual;
- mas navegable;
- mas explicable;
- mas cercana a un producto real;
- preparada para deploy cloud y Postgres.

## Frase de entrevista

"Primero construi una V1 funcional en Streamlit para probar el pipeline de analisis. Luego, en V2, mantuve ese nucleo y lo expuse con FastAPI y Next.js, anadiendo pricing dinamico, watchlist operativa, portfolio y set intelligence. La decision clave fue evolucionar incrementalmente sin reescribir lo que ya funcionaba."
