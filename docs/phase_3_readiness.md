# Preparación para Fase 3

Fecha: 2026-05-10

## Objetivo

Dejar el proyecto listo para empezar Fase 3 sin arrastrar deuda obvia de Fase 2.

Fase 3 debe centrarse en interfaz, vistas y experiencia de uso. Antes de eso, se hizo una limpieza mínima de datos y una regeneración de análisis reales con la captura corregida.

## Limpieza realizada

Durante la revisión cualitativa del scoring se detectó un registro antiguo con `shipping_eur=350.0`.

Ese valor venía de un bug ya corregido en `src/capture.py`: el parser confundía el precio del listing con el coste de envío cuando la palabra "envío" aparecía antes del precio.

Acción tomada:

- Registro afectado: `id=21`
- Acción: marcado como `discarded`
- Motivo: dato histórico contaminado por bug de captura

No se borró el registro para mantener trazabilidad.

## Regeneración con captura corregida

Se ejecutaron 5 URLs reales después de corregir el parser de envío.

| # | Set | Condición | Precio | Envío | Fair price | Margen neto | Score | Categoría |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | 75095 | SEALED | 350.00 EUR | N/D | 340.00 EUR | -52.00 EUR | 5 | RED |
| 2 | 75252 | SEALED | 850.00 EUR | N/D | 1200.00 EUR | 222.00 EUR | 70 | GREEN |
| 3 | 75095 | USED_COMPLETE | 173.00 EUR | N/D | 260.00 EUR | 53.00 EUR | 82 | GREEN |
| 4 | 75313 | SEALED | 1500.00 EUR | N/D | 1200.00 EUR | -428.00 EUR | 5 | RED |
| 5 | 75192 | USED_COMPLETE | 400.00 EUR | N/D | 720.00 EUR | 240.00 EUR | 97 | GREEN |

Resultado:

- 5 URLs reales probadas.
- 5 completaron el flujo end-to-end.
- 0 falsos costes de envío detectados.
- Casos GREEN y RED disponibles para revisar visualmente en la app.

## Estado técnico antes de Fase 3

- Pipeline end-to-end funcional.
- Anthropic operativo.
- SQLite operativo.
- App Streamlit mínima operativa.
- Catálogo inicial ampliado.
- Fair prices manuales disponibles para los sets principales de prueba.
- Scoring revisado cualitativamente.
- Parser de envío corregido.
- Tests automatizados pasando.

## Comando de verificación

```bash
pytest
```

Resultado actual:

```text
64 passed
```

## Qué debería incluir Fase 3

Fase 3 puede empezar sin tocar la lógica principal.

Prioridades recomendadas:

1. Mejorar presentación visual del resultado.
2. Separar claramente listings GREEN, YELLOW y RED.
3. Mostrar tabla de últimos analizados con columnas más útiles.
4. Permitir revisar detalles de un análisis guardado.
5. Mantener todo en una sola app Streamlit, sin React, sin Docker y sin arquitectura nueva.

## Qué no debería incluir Fase 3 todavía

- Scraping masivo.
- Crawlers.
- Automatización de compra.
- Postgres.
- pgvector.
- Dashboards complejos.
- Arquitectura enterprise.

## Decisión

El proyecto queda listo para empezar Fase 3.

La base técnica es suficiente para mejorar la experiencia de uso sin reescribir el núcleo.
