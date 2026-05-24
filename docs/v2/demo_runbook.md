# V2 demo runbook

Avance actual: **99/100**

Esta guia sirve para abrir y explicar LEGO Resale Intelligence V2 sin depender de memoria.

## Objetivo de la demo

Mostrar la evolucion de V1 a V2:

- V1 analizaba una URL y guardaba el resultado.
- V2 convierte esa base en una web tipo market intelligence terminal.
- V2 mantiene la arquitectura incremental: no reescribe V1, la reutiliza.

## Arranque local

Terminal 1 - API:

```bash
bash scripts/v2_start_api.sh
```

Terminal 2 - web:

```bash
bash scripts/v2_start_frontend.sh
```

Abrir:

```text
http://127.0.0.1:3000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Comprobar que todo responde:

```bash
bash scripts/v2_doctor.sh
```

## Recorrido recomendado

1. **Market**
   - Enseñar el dashboard general.
   - Explicar que consume portfolio, tendencias y briefing local.
   - Mostrar la UI 2D premium con lenguaje LEGO adulto sobrio.

2. **Analyze**
   - Explicar que reutiliza el pipeline V1.
   - Importante: analizar una URL real puede usar Anthropic.
   - Para una demo sin coste, usar `Load no-cost demo opportunity`.
   - Tras analizar o cargar demo, usar `Save to watchlist`.

3. **Watchlist**
   - Mostrar que la oportunidad guardada vive en SQLite.
   - Cambiar estado entre `watching`, `discarded` y `bought`.
   - Explicar que V1 y V2 comparten la misma base local.

4. **Sets**
   - Probar `75192`, `75313`, `75095` o `10214`.
   - Mostrar fair price, confianza, tendencia y grafico historico.

5. **Portfolio**
   - Mostrar coste, valor actual, P&L y senales HOLD/SELL.

6. **Briefings**
   - Explicar que usa briefing local por defecto.
   - Si existe `ANTHROPIC_API_KEY`, puede usar Claude Sonnet con fallback local.

## Coste de API

No gasta Anthropic:

- navegar por la web V2;
- abrir Market, Watchlist, Sets, Portfolio o Briefings;
- usar `Load no-cost demo opportunity` en Analyze;
- guardar en watchlist;
- cambiar estados;
- consultar APIs locales.

Puede gastar Anthropic:

- ejecutar `Analyze` con una URL real, porque llama al pipeline V1.

## Verificacion tecnica

```bash
.venv/bin/pytest
```

Resultado esperado actual:

```text
114 passed
```

```bash
cd frontend
npm run build
```

Resultado esperado:

```text
Compiled successfully
```

Doctor de rutas:

```bash
bash scripts/v2_doctor.sh
```

Resultado esperado:

```text
V2 looks healthy.
```

## Rutas V2

```text
/              Market Overview
/analyze       Listing analyzer
/watchlist     Deal workflow
/sets          Set Intelligence
/portfolio     Portfolio P&L
/briefings     Market briefing
```

## Endpoints clave

```text
GET    /health
POST   /api/analyze
POST   /api/analyze/demo
GET    /api/watchlist
POST   /api/watchlist
PATCH  /api/watchlist/{id}/status
GET    /api/market/set/{set_id}
GET    /api/market/history/{set_id}
GET    /api/portfolio
GET    /api/briefings
```

## Limitaciones honestas

- Los datos historicos son seed data, no mercado real en vivo.
- El portfolio tambien es seed data.
- SQLite es suficiente para demo local, pero no para producto cloud serio.
- El extractor sigue dependiendo del HTML de marketplaces externos.
- La capa de briefing aun no llama a Claude para evitar coste mientras se valida el producto.
