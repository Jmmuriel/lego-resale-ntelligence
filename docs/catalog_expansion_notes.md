# Notas de ampliación de catálogo

Fecha: 2026-05-10

## Objetivo

Ampliar de forma controlada la cobertura de la v1 técnica sin adelantar Fase 3.

El objetivo no es crear un catálogo completo de LEGO, sino reducir fallos por sets frecuentes que aparecen en listings reales y que el sistema ya puede analizar con la arquitectura actual.

## Sets añadidos

Se añadieron estos sets a `data/catalog.csv`:

- `75252` - Imperial Star Destroyer
- `75313` - AT-AT
- `75059` - Sandcrawler
- `10030` - Imperial Star Destroyer
- `75095` - TIE Fighter

Además, se añadieron referencias de fair price para sets que ya estaban en catálogo pero no tenían pricing:

- `10179` - Ultimate Collector's Millennium Falcon
- `10214` - Tower Bridge

## Criterio usado

Los precios son referencias manuales aproximadas en EUR para una v1 local.

No deben interpretarse como precio financiero definitivo. Sirven para:

- permitir que el pipeline end-to-end no se bloquee por falta de fair price;
- comparar oportunidades de forma consistente;
- probar el scoring con más variedad de listings;
- mantener una base simple y explicable.

## Fuentes de referencia

Se usaron referencias públicas de mercado secundario consultadas manualmente, principalmente BrickEconomy, y se redondearon valores para mantenerlos simples en EUR.

Los valores se separan por condición:

- `SEALED`
- `USED_COMPLETE`
- `USED_INCOMPLETE`
- `UNKNOWN`

## Regla de mantenimiento

Cuando se añada un set nuevo al catálogo, conviene añadir también su fair price en `src/pricing_reference.py`.

Si un set está en `data/catalog.csv` pero no tiene fair price, el pipeline puede identificarlo, pero no podrá calcular margen ni score.

## Próxima mejora razonable

Antes de Fase 3, se podría repetir este proceso con 10-20 sets más:

- Star Wars UCS frecuentes.
- LEGO Ideas retirados.
- Creator Expert / Icons retirados con buena liquidez.

La prioridad debe ser cobertura útil, no volumen.
