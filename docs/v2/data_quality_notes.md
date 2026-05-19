# V2 data quality notes

Avance demo local: **94/100**

Avance contra la guia completa: **76/100**

## Qué se ha hecho

Se añadió un validador automático para los datos seed de V2.

También se añadió un endpoint, una tarjeta en Market Overview y una página `Research` con búsqueda/filtros para ver la madurez de datos dentro de la app.

Además, cada candidato tiene ahora un checklist de promoción con 8 evidencias mínimas: año de salida, año de retirada, precio retail, piezas, popularidad, 2 fuentes de metadata, 2 fuentes de precio y 3 snapshots de mercado.

Comando:

```bash
.venv/bin/python scripts/v2_validate_seed_data.py
```

## Qué revisa

- Que `data/catalog.csv` tenga columnas obligatorias.
- Que no haya sets duplicados.
- Que años, piezas, precios retail y popularidad tengan formato válido.
- Que `data/price_history_seed.json` use sets existentes en catálogo.
- Que cada banda de precio cumpla `min <= avg <= max`.
- Que `data/portfolio_seed.json` use sets existentes en catálogo.
- Que no haya posiciones de portfolio con IDs duplicados.

## Estado actual

Resultado actual:

```text
V2 seed data validation: OK
catalog_sets: 10
catalog_candidate_sets: 40
catalog_plus_candidates: 50
target_catalog_sets: 50
price_snapshots: 12
priced_sets: 4
candidate_ready_for_promotion: 0
portfolio_items: 3
portfolio_sets: 3
sets_with_3_plus_snapshots: 3
sets_with_5_plus_snapshots: 1
WARNING CATALOG_BELOW_TARGET: Catalog has 10 sets; guide target is 50.
```

Esto significa:

- los datos actuales son consistentes;
- la demo puede seguir funcionando;
- hay 40 candidatos pendientes de investigar antes de activarlos en el catálogo.
- ahora mismo 0 candidatos están listos para promoción, porque no hemos cargado evidencias verificadas.

## Por qué mejora la guía completa

Antes podíamos añadir datos, pero no teníamos una alarma clara si algo quedaba mal.

Ahora podemos crecer el catálogo y el histórico con más confianza. Cuando metamos 50 sets, el script nos dirá si falta precio, si un set no existe o si una fila tiene formato incorrecto. El nuevo candado de candidatos evita además que pasemos un set a catálogo activo sin evidencias mínimas.

## Siguiente paso recomendado

**G4B - validar candidatos y promoverlos al catálogo activo.**

Para precios reales de mercado, conviene validarlos manualmente con BrickLink o una fuente equivalente antes de tratarlos como fair price.
