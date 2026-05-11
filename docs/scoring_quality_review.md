# Revisión cualitativa del scoring

Fecha: 2026-05-10

## Objetivo

Revisar si el score actual se comporta de forma razonable antes de tocar la fórmula o pasar a Fase 3.

La revisión se basa en resultados reales guardados en SQLite durante las validaciones de Fase 2.

## Fórmula actual

El score parte del margen neto porcentual:

```text
margen neto = fair price - comisión estimada - envío de salida - coste de adquisición
```

Después:

- margen neto porcentual menor o igual a 0 -> score base 0;
- margen neto porcentual igual o superior a 40% -> score base 100;
- entre 0% y 40% -> escala lineal;
- penalización por riesgos;
- pequeña bonificación por marketplace conocido.

La categoría final es:

- `GREEN`: score >= 70 y margen neto > 20 EUR;
- `YELLOW`: score entre 45 y 69;
- `RED`: resto.

## Casos GREEN revisados

| Set | Condición | Precio pedido | Fair price | Margen neto | Score | Lectura |
|---|---|---:|---:|---:|---:|---|
| 75095 | USED_COMPLETE | 173.00 EUR | 260.00 EUR | 53.00 EUR | 82 | Tiene margen real sobre un ticket pequeño; GREEN razonable. |
| 75252 | SEALED | 850.00 EUR | 1200.00 EUR | 222.00 EUR | 70 | Buen margen absoluto; GREEN razonable. |
| 75192 | USED_COMPLETE | 450.00 EUR | 720.00 EUR | 190.00 EUR | 100 | Muy buen margen; GREEN razonable. |
| 75192 | USED_COMPLETE | 400.00 EUR | 720.00 EUR | 240.00 EUR | 97 | Buen margen, aunque con riesgo `Sin caja original`; GREEN razonable pero requiere revisión manual. |

## Casos RED revisados

| Set | Condición | Precio pedido | Fair price | Margen neto | Score | Lectura |
|---|---|---:|---:|---:|---:|---|
| 75059 | USED_COMPLETE | 360.00 EUR | 380.00 EUR | -26.00 EUR | 0 | Margen negativo y caja dañada; RED correcto. |
| 75313 | SEALED | 1500.00 EUR | 1200.00 EUR | -428.00 EUR | 5 | Muy caro frente al fair price; RED correcto. |
| 21309 | SEALED | 250.00 EUR | 135.00 EUR | -136.50 EUR | 5 | Muy caro frente al fair price; RED correcto. |
| 10221 | SEALED | 1150.00 EUR | 650.00 EUR | -573.00 EUR | 5 | Muy caro frente al fair price; RED correcto. |
| 75192 | SEALED | 750.00 EUR | 880.00 EUR | 34.00 EUR | 16 | Margen positivo pero bajo respecto al capital invertido; RED conservador y defendible. |

## Hallazgo de calidad de datos

Durante la revisión apareció un caso antiguo con `shipping_eur=350.0`.

Ese valor no era un envío real: el parser había confundido el precio del listing con envío porque la palabra "envío" aparecía antes del precio en el texto de la página.

Corrección aplicada:

- `src/capture.py` ahora solo captura envío si el importe está muy cerca de la palabra envío/shipping o si indica gratis/free.
- Se añadió un test específico para evitar esta regresión.

No se han reescrito registros históricos en SQLite. Para análisis serio, conviene interpretar esos registros antiguos con cautela o regenerarlos.

## Conclusión

El scoring actual se comporta de forma razonable para una v1:

- detecta oportunidades con margen real;
- descarta listings caros;
- penaliza riesgos;
- evita marcar como GREEN casos con margen absoluto demasiado bajo;
- mantiene una lógica simple y explicable.

No recomiendo cambiar la fórmula todavía.

## Siguiente mejora recomendada

Antes de tocar el scoring, conviene mejorar la calidad de datos:

1. añadir más sets y fair prices;
2. limpiar o regenerar registros antiguos con errores de captura;
3. seguir probando URLs reales;
4. solo ajustar la fórmula si aparecen patrones repetidos de falsos GREEN o falsos RED.
