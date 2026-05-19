# V2 release checklist

Avance demo local: **94/100**

Avance contra la guía completa: **76/100**

Checklist para pasar de demo local a version ensenable/publicable.

## Listo

- [x] API FastAPI con `/health`.
- [x] Reutilizacion del pipeline V1 desde `POST /api/analyze`.
- [x] Pricing dinamico seed.
- [x] Set Intelligence con grafico historico.
- [x] Portfolio seed con P&L.
- [x] Briefings locales sin coste de LLM.
- [x] Frontend Next.js con rutas principales.
- [x] Escena 3D inicial en Market.
- [x] Watchlist compartida con SQLite V1.
- [x] Tests backend/core pasando.
- [x] Build frontend pasando.
- [x] README principal explica V1 y V2.
- [x] Runbook de demo local.
- [x] Scripts simples para arrancar API/frontend.
- [x] Doctor de rutas V2.
- [x] Variables frontend documentadas en `frontend/.env.example`.
- [x] Demo Analyze sin coste de Anthropic.
- [x] Narrativa de portfolio V1 -> V2.
- [x] Plan de deploy V2.
- [x] PostgreSQL/Alembic foundation en código.
- [x] Migración inicial V2 verificada localmente.
- [x] Seed data migrable a tablas V2.
- [x] Pricing y portfolio leen DB V2 con fallback JSON.
- [x] Validación automática de seed data V2.
- [x] Lista candidata para expandir de 10 a 50 sets.
- [x] Endpoint y UI de madurez de datos.
- [x] Página Research filtrable para revisar candidatos sin activarlos.
- [x] Checklist de promoción segura para candidatos de catálogo.

## Antes de publicar

- [ ] Hacer capturas V2 desktop.
- [ ] Hacer capturas V2 mobile.
- [x] Revisar copy final en ingles/espanol.
- [x] Decidir si se publica V2 en el mismo README o en case study separado.
- [x] Crear variables `.env.example` especificas para V2 si hacen falta.
- [x] Decidir deploy:
  - backend: Railway, Render o Fly.io;
  - frontend: Vercel;
  - base de datos: SQLite solo demo local o Postgres para persistencia real.
- [x] Migrar seed data a tablas reales si se usa Postgres o SQLite V2.
- [x] Conectar servicios principales a DB V2 con fallback local.
- [ ] Revisar permisos y no subir `.env`, `.next`, `node_modules` ni base SQLite local.

## Criterio para 90/100

V2 alcanza 90/100 cuando:

- README principal explica V1 y V2 con claridad;
- demo runbook existe;
- rutas principales estan verificadas;
- hay checklist de publicacion;
- no quedan bloqueos locales de Node/npm.

## Criterio para 95/100

V2 alcanza 95/100 cuando:

- hay capturas finales;
- hay narrativa de portfolio V1 -> V2;
- hay instrucciones de deploy;
- hay datos demo suficientes para no depender de URLs reales.

## Criterio para 100/100

V2 alcanza 100/100 cuando:

- esta publicada o lista para publicar;
- README, capturas y demo estan cerrados;
- la historia tecnica se puede explicar en entrevista en menos de 5 minutos;
- las limitaciones estan documentadas con honestidad.
