# Manual simple para publicar V2

Avance demo local: **99/100**

Avance contra la guia completa: **90/100**

Este documento es para publicar LEGO Resale Intelligence V2 sin saber programacion.

## Idea simple

La app V2 son dos piezas:

- **Railway**: publica la API, que es el motor.
- **Vercel**: publica la web, que es lo que ve el usuario.

Opcionalmente:

- **Postgres en Railway**: guarda datos editables en la nube.

## Antes de tocar nada

La app local ya esta lista para demo:

- web local: `http://127.0.0.1:3000`
- API local: `http://127.0.0.1:8000/docs`
- tests: `116 passed`
- build frontend: OK
- doctor V2: OK
- smoke test local: OK

Importante: venderlo como **seed-backed prototype**, no como plataforma de precios reales verificados.

## Paso 1 - Railway backend

1. Entrar en Railway.
2. Crear nuevo proyecto.
3. Elegir deploy desde GitHub.
4. Seleccionar este repo.
5. Railway debe detectar el `Dockerfile`.
6. Si Railway pregunta por comando, usar:

```bash
sh scripts/v2_boot_api.sh
```

7. Añadir variables:

```env
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
BACKEND_CORS_ORIGINS=https://lego-resale-ntelligence.vercel.app
V2_RUN_MIGRATIONS=0
V2_SEED_DATABASE=0
```

Para demo sin IA real, `ANTHROPIC_API_KEY` puede quedarse vacia.

## Paso 2 - Railway Postgres opcional

Solo hace falta si quieres persistencia cloud real.

1. En Railway, añadir servicio Postgres.
2. Copiar la URL de conexion.
3. Ponerla como:

```env
V2_DATABASE_URL=postgresql+psycopg://...
```

4. Para el primer deploy con base nueva:

```env
V2_RUN_MIGRATIONS=1
V2_SEED_DATABASE=1
```

5. Despues del primer deploy correcto, cambiar:

```env
V2_SEED_DATABASE=0
```

Esto evita sobrescribir datos editados en cada redeploy.

## Paso 3 - Vercel frontend

1. Entrar en Vercel.
2. Crear nuevo proyecto desde GitHub.
3. Seleccionar este repo.
4. Configurar Root Directory:

```text
frontend
```

5. Build command:

```bash
npm run build
```

6. Añadir variable:

```env
NEXT_PUBLIC_API_URL=https://lego-resale-ntelligence-production.up.railway.app
```

## Paso 4 - Conectar Railway y Vercel

Cuando Vercel ya tenga URL final, volver a Railway y actualizar:

```env
BACKEND_CORS_ORIGINS=https://lego-resale-ntelligence.vercel.app
```

Si se usa dominio propio, añadir ese dominio tambien separado por coma:

```env
BACKEND_CORS_ORIGINS=https://lego-resale-ntelligence.vercel.app,https://tudominio.com
```

## Paso 5 - Probar publicacion

Cuando tengas las dos URLs:

```bash
API_URL=https://lego-resale-ntelligence-production.up.railway.app \
WEB_URL=https://lego-resale-ntelligence.vercel.app \
sh scripts/v2_deploy_smoke.sh
```

Tiene que salir todo con `ok`.

## Qué decir en portfolio

Frase buena:

> Seed-backed LEGO resale intelligence prototype with production-style architecture, data-quality gates and portfolio workflows.

No decir todavia:

> Verified live LEGO market pricing platform.

## Qué queda para 100/100

- Publicar backend en Railway.
- Publicar frontend en Vercel.
- Probar URLs publicas con `scripts/v2_deploy_smoke.sh`.
- Decidir si `75192` debe estar como set activo/retiring o retirado.
- Verificar mas sets con fuentes reales.
