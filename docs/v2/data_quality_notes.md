# V2 data quality notes

Avance demo local: **99/100**

Avance contra la guia completa: **90/100**

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
catalog_sets: 50
catalog_candidate_sets: 0
catalog_plus_candidates: 50
target_catalog_sets: 50
price_snapshots: 250
priced_sets: 50
candidate_ready_for_promotion: 0
portfolio_items: 3
portfolio_sets: 3
sets_with_3_plus_snapshots: 50
sets_with_5_plus_snapshots: 50
unpriced_catalog_sets: []
active_catalog_verified_sets: 32
active_catalog_verified_pct: 64.0
active_catalog_evidence_started_sets: 50
active_catalog_blocked_sets: 18
market_data_source_status: partially_verified
```

Esto significa:

- los datos seed actuales son consistentes;
- la demo puede seguir funcionando;
- el catálogo seed llega al objetivo local de 50 sets;
- la app distingue entre datos seed/demo y datos externamente verificados;
- FASE DATA-1 ya auditó 50 sets del catálogo activo;
- DATA-2 normalizó discrepancias seguras del CSV contra las evidencias guardadas;
- 32 sets pasan como verificados bajo las reglas actuales de la app;
- 18 sets quedan bloqueados o en revisión por discrepancias de fuentes;
- ahora mismo no hay candidatos pendientes en `data/catalog_expansion_candidates.csv`.

## Por qué mejora la guía completa

Antes podíamos añadir datos, pero no teníamos una alarma clara si algo quedaba mal.

Ahora podemos crecer el catálogo y el histórico con más confianza. El script nos dice si falta precio, si un set no existe o si una fila tiene formato incorrecto. El candado de candidatos evita además que pasemos futuros candidatos a catálogo activo sin evidencias mínimas.

Nota honesta para portfolio: los 50 sets actuales deben presentarse como **seed/demo data** salvo que se añadan evidencias explícitas de fuentes en `data/catalog_active_research.json`. El archivo `data/catalog_candidate_research.json` queda para futuros candidatos antes de activarlos.

El histórico `data/price_history_seed.json` usa ahora `manual_seed_reference` para evitar sugerir que las cifras proceden de BrickLink si no hay evidencia guardada.

Primera auditoria real:

- `75192` tiene fuentes de metadata/precio localizadas, pero no se marca como verificado;
- bloqueo: el catálogo seed dice `year_retired = 2024`, mientras BrickRanker y la página oficial de LEGO apuntan a set activo / retirada estimada en 2026;
- acción recomendada: separar en V2 los sets realmente retirados de los sets activos o en vigilancia de retirada.

## Siguiente paso recomendado

**G4C - etiquetar evidencias/fuentes de los 50 sets seed antes de publicarlos como datos reales.**

Para precios reales de mercado, conviene validarlos manualmente con BrickLink o una fuente equivalente antes de tratarlos como fair price.
