# Tareas manuales V2

Avance demo local: **99/100**

Avance contra la guía completa: **90/100**

Esta lista es para separar claramente qué hace Codex y qué debe hacer Juan manualmente.

## Ahora mismo

No tienes que hacer nada manual ahora mismo.

La foundation PostgreSQL/Alembic ya esta creada en codigo y verificada en SQLite local. Además, pricing y portfolio ya leen desde la DB V2 cuando hay datos cargados.

Cuando pasemos a Postgres real, probablemente sí tendré que pedirte una de estas dos cosas:

- instalar/abrir Postgres local en el Mac;
- o crear una base Postgres en Railway.

Dirección visual elegida:

- inspiración: Linear + Stripe;
- lenguaje LEGO adulto, no infantil;
- UI 2D premium, sin 3D;
- nombre interno: Collector Terminal.

Bloqueo resuelto:

- Node está disponible;
- npm está disponible;
- el frontend Next.js ya instala dependencias y compila;
- la API y la web ya se pueden abrir en local;
- la web ya tiene rutas reales para Market, Analyze, Sets, Portfolio y Briefings;
- la ficha Sets ya enseña gráfico de histórico de precios;
- Analyze ya puede guardar oportunidades en la watchlist compartida con V1;
- Analyze ya tiene una oportunidad demo que no gasta Anthropic;
- Watchlist ya permite filtrar registros y cambiar estados desde V2;
- existe guia de demo local para ensenar la V2;
- existe checklist de publicacion;
- existen scripts simples para arrancar y comprobar V2;
- existe narrativa de portfolio;
- existe plan de deploy V2;
- pricing y portfolio leen desde DB V2 con fallback JSON;
- existe validación automática de datos seed antes de cargar DB V2;
- existe checklist de 8 evidencias para no promocionar candidatos sin datos verificados;
- no se han tocado carpetas fuera del proyecto para continuar.

## Más adelante

Probablemente necesitaré que hagas estas cosas:

1. Crear o confirmar un repo GitHub público cuando toque publicar V2.
2. Crear cuenta o proyecto en Railway para backend y PostgreSQL.
3. Crear cuenta o proyecto en Vercel para frontend.
4. En Railway, configurar:
   - `V2_DATABASE_URL` si se usa Postgres;
   - `BACKEND_CORS_ORIGINS` con la URL final de Vercel;
   - `V2_RUN_MIGRATIONS=1` para el primer deploy;
   - `V2_SEED_DATABASE=1` solo para el primer seed.
5. En Vercel, configurar:
   - Root Directory: `frontend`;
   - `NEXT_PUBLIC_API_URL` con la URL final de Railway.
6. Después del primer seed en Railway, cambiar `V2_SEED_DATABASE=0`.
4. Conseguir o confirmar la API key de Anthropic.
5. Revisar datos reales de portfolio si quieres que el P&L sea creíble.
6. Validar manualmente algunos precios de BrickLink antes de usarlos como seed.

Cuando llegue cada momento, te lo diré con instrucciones simples y paso a paso.
