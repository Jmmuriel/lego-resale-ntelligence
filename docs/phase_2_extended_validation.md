# Validación extendida de Fase 2 - Catálogo ampliado

Fecha: 2026-05-10

## Objetivo

Validar que la ampliación controlada del catálogo mejora la cobertura real de la app sin empezar Fase 3.

Esta prueba se hizo después de añadir referencias para sets adicionales como:

- `75252` - Imperial Star Destroyer
- `75313` - AT-AT
- `75059` - Sandcrawler
- `75095` - TIE Fighter
- `10030` - Imperial Star Destroyer
- `10214` - Tower Bridge

## Resultado de la prueba

Se probaron 10 URLs reales de Wallapop con sets del catálogo ampliado.

| # | URL | Resultado | Observación |
|---|---|---|---|
| 1 | https://es.wallapop.com/item/lego-75252-imperial-star-destroyer-nuevo-1192865701 | Funciona | Set `75252`, `SEALED`, score `70`, categoría `GREEN`. |
| 2 | https://es.wallapop.com/item/lego-star-wars-75252-destructor-imperial-1155936877 | Falla | Wallapop devuelve `404 Not Found`. |
| 3 | https://es.wallapop.com/item/lego-75313-at-at-star-wars-ucs-1096932728 | Funciona | Set `75313`, `SEALED`, score `5`, categoría `RED`. |
| 4 | https://es.wallapop.com/item/lego-75313-star-wars-1196473544 | Falla | Wallapop devuelve `404 Not Found`. |
| 5 | https://es.wallapop.com/item/lego-star-wars-sandcrawler-75059-1183134138 | Funciona | Set `75059`, `USED_COMPLETE`, score `0`, categoría `RED`. |
| 6 | https://es.wallapop.com/item/lego-star-wars-75059-sandcrawler-ucs-1183024386 | Falla | Wallapop devuelve `404 Not Found`. |
| 7 | https://es.wallapop.com/item/lego-star-wars-75095-tie-fighter-ucs-montado-1183084023 | Funciona | Set `75095`, `USED_COMPLETE`, score `82`, categoría `GREEN`. |
| 8 | https://es.wallapop.com/item/lego-star-wars-75095-tie-fighter-1097903965 | Funciona | Set `75095`, `SEALED`, score `5`, categoría `RED`. |
| 9 | https://es.wallapop.com/item/lego-star-wars-ucs-10030-1155566711 | Falla | Wallapop devuelve `404 Not Found`. |
| 10 | https://es.wallapop.com/item/lego-10214-tower-bridge-1187578355 | Falla | Wallapop devuelve `404 Not Found`. |

## Resumen

- URLs reales probadas: 10
- Flujo end-to-end completado: 5
- Fallos externos por `404`: 5
- Nuevos sets validados end-to-end: `75252`, `75313`, `75059`, `75095`
- Categorías generadas: `GREEN` y `RED`
- Guardado en SQLite: confirmado

## Lectura de producto

La ampliación del catálogo sí mejora la utilidad de la app: ahora el sistema puede analizar oportunidades fuera de los tres sets iniciales.

La principal limitación sigue siendo externa:

- muchos listings reales desaparecen;
- Wallapop puede devolver `404`;
- eBay sigue siendo problemático por bloqueos;
- el parser HTML depende de lo que cada marketplace exponga.

## Conclusión

El siguiente cuello de botella ya no es solo el scoring ni la persistencia.

Los próximos riesgos principales son:

1. cobertura de catálogo;
2. calidad de referencias de fair price;
3. robustez de captura HTML;
4. validación manual de si el score coincide con intuición de compra.

Antes de invertir en UI de Fase 3, conviene hacer una última mini-validación cualitativa:

- revisar 5 casos `GREEN`;
- revisar 5 casos `RED`;
- decidir si el score se siente razonable;
- ajustar constants de scoring solo si hay evidencia.
