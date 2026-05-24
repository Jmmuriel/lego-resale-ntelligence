# LEGO Resale Intelligence V2

Estado actual: **Frontend V2 funcionando en local**

Avance demo local: **99/100**

Avance contra la guía completa: **90/100**

## Qué estamos haciendo

V2 no empieza reescribiendo la app. Empieza ordenando el proyecto para que la V1 siga viva y la V2 pueda crecer encima.

La decisión actual es:

- mantener **un solo repo**;
- conservar la V1 de Streamlit como demo legacy;
- construir V2 en carpetas nuevas cuando toque:
  - `backend/` para FastAPI;
  - `frontend/` para Next.js;
  - `docs/v2/` para la guía, decisiones y roadmap.

## Guía original

La guía maestra V2 está guardada aquí:

- `docs/v2/lego_resale_intelligence_v2_guide.pdf`

Esa guía es el norte estratégico. El plan de implementación adaptado a este repo está en:

- `docs/v2/implementation_plan.md`
- `docs/v2/database_decision.md`
- `docs/v2/pricing_engine_notes.md`
- `docs/v2/portfolio_notes.md`
- `docs/v2/briefing_notes.md`
- `docs/v2/ui_direction.md`
- `docs/v2/demo_runbook.md`
- `docs/v2/release_checklist.md`
- `docs/v2/portfolio_story.md`
- `docs/v2/deploy_plan.md`
- `docs/v2/final_handoff.md`
- `docs/v2/guide_gap_analysis.md`
- `docs/v2/postgres_alembic_notes.md`
- `docs/v2/db_read_fallback_notes.md`
- `docs/v2/data_quality_notes.md`

## Regla de trabajo

Cada fase tiene que dejar algo funcional o una decisión clara. Si una fase no se puede explicar fácil, está demasiado grande.

## Próximo paso

Bloque actual:

**Frontend/UI V2**: app visual preparada y compilada.

Dirección visual definida:

- inspiración principal: Linear + Stripe;
- lenguaje LEGO adulto y sobrio;
- nombre interno: Collector Terminal;
- UI 2D premium, sin escena 3D.

Estado técnico actual:

1. Node y npm ya están disponibles localmente;
2. dependencias de frontend instaladas en `frontend/`;
3. `npm run build` compila correctamente;
4. backend FastAPI corre en `http://127.0.0.1:8000`;
5. frontend Next.js corre en `http://127.0.0.1:3000`;
6. Market Overview ya consume la API tipada;
7. existen rutas V2 para `Market`, `Analyze`, `Sets`, `Portfolio` y `Briefings`;
8. la home usa un dashboard 2D premium sin Three.js;
9. `Set Intelligence` muestra fair price, confianza, tendencia y resumen por set;
10. `Set Intelligence` incluye gráfico de histórico de precio medio;
11. `Analyze` permite guardar resultados en la watchlist SQLite compartida con V1;
12. `Analyze` incluye una oportunidad demo sin coste de Anthropic;
13. `Watchlist` permite filtrar oportunidades y cambiar estado desde V2;
14. existe runbook de demo V2;
15. existe checklist de publicacion V2;
16. existen scripts simples para arrancar API, web y comprobar rutas;
17. existe `frontend/.env.example`;
18. existe narrativa de portfolio V1 -> V2;
19. existe plan de deploy V2;
20. existe base PostgreSQL/Alembic inicial;
21. existe script de carga seed a DB V2;
22. pricing y portfolio leen DB V2 primero con fallback a JSON;
23. existe validador de calidad para catálogo, precios y portfolio;
24. el catálogo activo seed ya llega a 50 sets;
25. existe endpoint y tarjeta UI de madurez de datos;
26. existe página `Research` para futuras colas de candidatos;
27. existe checklist de promoción segura por candidato cuando haya candidatos nuevos;
28. `.gitignore` protege `node_modules`, `.next` y secretos locales;
29. existe auditoría activa de evidencias en `data/catalog_active_research.json`;
30. existe endpoint `/api/market/active-evidence`;
31. existe preparación de deploy para Railway/Vercel con `.dockerignore`, boot script y smoke test.
32. existe case study V2 en Markdown y HTML;
33. existe handoff final con estado real, limites y pasos manuales.

Próximo paso:

1. resolver la discrepancia de retirada de `75192` antes de marcarlo como verificado;
2. ampliar hacia 300+ sets solo con evidencias;
3. crear proyecto Railway y Vercel cuando toque publicación;
4. preparar Postgres real cuando toque persistencia cloud;
5. preparar capturas V2 desktop/mobile y case study final.
