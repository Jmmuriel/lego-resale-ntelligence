# Briefings V2

Avance V2: **55/100**

Fecha: 2026-05-14

## Estado

Briefing mínimo implementado sin coste de API.

El sistema ya puede generar un briefing ejecutivo a partir de:

- movimientos de precio;
- resumen de portfolio;
- señal dominante de portfolio;
- acción recomendada.

## Qué se añadió

- `backend/services/ai_analyst.py`
- endpoint `GET /api/briefings`
- endpoint `POST /api/briefings/generate`
- tests en `tests/test_ai_analyst.py`

## Qué significa en sencillo

V2 ya puede producir un resumen tipo analista:

- qué está pasando en precios;
- cómo está el portfolio;
- qué acción conviene revisar.

Todavía no estamos usando Anthropic para generarlo. Lo hacemos localmente para validar la estructura sin gastar saldo.

## Por qué no se usa Anthropic todavía

Para evitar gasto innecesario mientras estamos construyendo.

La API devuelve:

- `used_llm: false`
- `token_count: 0`
- `model_version: local-deterministic-v0`

Cuando activemos Claude Sonnet, cambiaremos esos campos y añadiremos control de coste.

## Qué estructura tiene el briefing

- Resumen ejecutivo
- Movimientos de mercado
- Portfolio
- Acción recomendada

## Próximo paso técnico futuro

Conectar este mismo contexto a Claude Sonnet:

1. construir payload estructurado;
2. llamar a Anthropic solo bajo acción explícita;
3. limitar tokens;
4. guardar token count;
5. conservar fallback local si falla el modelo.
