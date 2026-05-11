# Validación de Fase 2 - LEGO Resale Intelligence

Fecha de validación: 2026-05-10

## Objetivo

Cerrar formalmente la Fase 2 del proyecto con una prueba manual end-to-end usando URLs reales.

La Fase 2 no busca una UI premium ni dashboards avanzados. Su objetivo es demostrar que el flujo técnico mínimo funciona:

```text
URL real -> captura HTML -> parsing básico -> extracción LLM -> identificación de set -> fair price -> scoring -> SQLite -> Streamlit
```

## Estado del proyecto

La app ya ejecuta el flujo completo desde una pantalla mínima de Streamlit:

- El usuario pega una URL real de listing.
- El sistema descarga el HTML con `requests`.
- El parser extrae título, descripción, precio y marketplace cuando están disponibles.
- Anthropic convierte el texto crudo en una extracción estructurada.
- El sistema identifica el set contra `data/catalog.csv`.
- El sistema obtiene un fair price manual desde `src/pricing_reference.py`.
- El sistema calcula margen bruto, margen neto, score y categoría.
- El resultado se guarda en SQLite.
- Streamlit muestra el análisis y una tabla con los últimos listings analizados.

## Piezas incluidas en Fase 2

- `src/capture.py`: captura HTML individual y parser básico.
- `src/extract.py`: extracción estructurada con Anthropic.
- `src/identify.py`: matching contra catálogo local.
- `data/catalog.csv`: catálogo mínimo de sets LEGO retirados.
- `src/pricing_reference.py`: referencias manuales de fair price.
- `src/scoring.py`: cálculo de márgenes, score y categoría.
- `src/pipeline.py`: orquestación end-to-end.
- `src/db.py`: SQLite local con CRUD básico.
- `app/main.py`: Streamlit mínimo para analizar una URL y ver últimos resultados.
- `tests/`: cobertura mínima de modelos, captura, extracción, identificación, scoring, pipeline y base de datos.

## Checklist de test manual con 10 URLs reales

| # | URL | Resultado | Causa / observación |
|---|---|---|---|
| 1 | https://es.wallapop.com/item/lego-star-wars-ucs-millennium-falcon-75192-1140786697 | Funciona | Set `75192`, categoría `RED`, margen neto negativo. |
| 2 | https://es.wallapop.com/item/lego-75192-741928457 | Funciona | Set `75192`, categoría `RED`, margen neto ligeramente negativo. |
| 3 | https://es.wallapop.com/item/lego-star-wars-75192-891413866 | Falla | Wallapop devuelve `404 Not Found`; el listing no está accesible. |
| 4 | https://es.wallapop.com/item/lego-ucs-millennium-falcon-75192-1173945927 | Funciona | Set `75192`, categoría `GREEN`, margen neto positivo. |
| 5 | https://es.wallapop.com/item/lego-star-wars-millennium-falcon-ucs-75192-1196379171 | Funciona | Set `75192`, categoría `RED`, margen neto positivo pero score bajo. |
| 6 | https://es.wallapop.com/item/lego-star-wars-halcon-milenario-75192-1167711336 | Funciona | Set `75192`, categoría `RED`, margen neto positivo pero score bajo. |
| 7 | https://es.wallapop.com/item/star-war-lego-halcon-milenario-75192-ucs-1039011732 | Funciona | Set `75192`, categoría `GREEN`, margen neto positivo. |
| 8 | https://es.wallapop.com/item/lego-star-wars-10221-super-star-destroyer-ucs-975470614 | Funciona | Set `10221`, categoría `RED`, margen neto negativo. |
| 9 | https://es.wallapop.com/item/lego-star-wars-10221-super-star-destroyer-1119924693 | Falla | Wallapop devuelve `404 Not Found`; el listing no está accesible. |
| 10 | https://es.wallapop.com/item/lego-ideas-21309-nasa-apollo-saturn-v-nuevo-1074350525 | Funciona | Set `21309`, categoría `RED`, margen neto negativo. |

## Resumen de resultados

- URLs reales probadas: 10
- Flujo end-to-end completado: 8
- Fallos controlados: 2
- Causa de fallos: listings reales no accesibles (`404 Not Found`)
- Marketplaces probados en cierre: Wallapop
- Guardado en SQLite: confirmado
- Uso real de Anthropic: confirmado
- Tests automatizados: `60 passed`

## Resultados guardados representativos

| Set | Condición | Precio pedido | Fair price | Margen neto | Score | Categoría |
|---|---|---:|---:|---:|---:|---|
| 75192 | USED_COMPLETE | 900.00 EUR | 720.00 EUR | -260.00 EUR | 0 | RED |
| 75192 | SEALED | 799.95 EUR | 880.00 EUR | -15.95 EUR | 5 | RED |
| 75192 | USED_COMPLETE | 400.00 EUR | 720.00 EUR | 240.00 EUR | 97 | GREEN |
| 75192 | USED_COMPLETE | 450.00 EUR | 720.00 EUR | 190.00 EUR | 100 | GREEN |
| 10221 | SEALED | 1150.00 EUR | 650.00 EUR | -573.00 EUR | 5 | RED |
| 21309 | SEALED | 250.00 EUR | 135.00 EUR | -136.50 EUR | 5 | RED |

## Limitaciones actuales

- El catálogo local es pequeño. Si el set no existe en `data/catalog.csv`, el flujo no puede identificarlo.
- El fair price es manual y vive en `src/pricing_reference.py`; todavía no se carga desde CSV ni base de datos.
- El parser HTML es básico y depende de lo que cada marketplace exponga en el HTML.
- eBay puede bloquear requests con `403 Forbidden`.
- Listings reales pueden desaparecer o devolver `404`.
- El score es una primera versión simple y explicable, no una valoración financiera definitiva.
- La app todavía no tiene UI premium, filtros avanzados ni vistas múltiples; eso pertenece a Fase 3.

## Criterio de cierre de Fase 2

Fase 2 se considera cerrada si se cumplen estos puntos:

- Existe captura HTML individual sin crawler masivo.
- Existe extracción estructurada con Anthropic.
- Existe identificación contra catálogo local.
- Existe cálculo de pricing, margen y scoring.
- Existe SQLite local con guardado y listado básico.
- Existe app Streamlit mínima con input de URL y tabla de últimos analizados.
- Existe test manual con 10 URLs reales y resultados documentados.
- Los fallos externos quedan identificados y no rompen el criterio técnico de la fase.

## Decisión

Fase 2 queda cerrada como v1 técnica local y defendible.

No es todavía una herramienta productiva completa. Es una base funcional para aprender, iterar y decidir si merece pasar a Fase 3.

## Próximo paso recomendado

Antes de empezar Fase 3, conviene hacer una ampliación pequeña y controlada:

- Añadir 10-20 sets frecuentes al catálogo local.
- Añadir fair prices manuales para esos sets.
- Repetir la prueba con listings más variados.

Después de eso, Fase 3 puede centrarse en UI, vistas, filtros y presentación visual.
