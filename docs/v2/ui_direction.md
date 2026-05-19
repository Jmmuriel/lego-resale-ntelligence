# Dirección visual V2 - Collector Terminal

Avance V2: **58/100**

Fecha: 2026-05-14

## Idea central

LEGO Resale Intelligence V2 debe sentirse como una terminal premium de mercado para coleccionismo LEGO retirado.

No es una web infantil. No es una juguetería. Es una herramienta de inteligencia para tomar mejores decisiones sobre sets retirados.

Nombre interno de la dirección:

**Collector Terminal**

## Referencias principales

### Linear

Qué tomamos:

- navegación limpia;
- jerarquía clara;
- sensación de producto profesional;
- interfaces densas pero calmadas;
- dark mode elegante;
- microinteracciones discretas.

### Stripe

Qué tomamos:

- pulido visual;
- confianza financiera;
- tratamiento serio de datos y métricas;
- cards limpias;
- uso inteligente del color;
- sensación de producto caro.

### LEGO adulto

Qué tomamos:

- color LEGO como acento;
- modularidad visual inspirada en bricks;
- studs como motivo gráfico;
- idea de set como objeto coleccionable;
- tono adulto, de colección y valor, no de juego infantil.

## Personalidad visual

La interfaz debe sentirse:

- premium;
- precisa;
- coleccionista;
- financiera;
- táctil;
- calmada;
- seria pero con alma LEGO.

No debe sentirse:

- infantil;
- saturada;
- genérica SaaS;
- dashboard barato;
- landing de juguete;
- catálogo de e-commerce común.

## Paleta propuesta

Base:

- `ink`: #080A0F
- `graphite`: #111827
- `surface`: #F7F4EC
- `surface-soft`: #FFFDF7
- `line`: rgba(8, 10, 15, 0.12)

LEGO accents:

- `lego-yellow`: #F7C600
- `lego-red`: #D01012
- `brick-black`: #050505

Signals:

- `signal-green`: #13A067
- `signal-amber`: #D99000
- `signal-red`: #D92D20
- `info-blue`: #3B82F6

Uso:

- amarillo LEGO para valor, score y highlights;
- rojo LEGO con mucho cuidado para riesgo o marca;
- verde/amber/rojo para señales financieras;
- fondos sobrios, no bañados en color.

## Lenguaje LEGO sin infantilizar

Usaremos LEGO en detalles concretos:

- grid modular inspirado en piezas 2x4, 2x2 y 1x2;
- badges con forma o sombra sutil de stud;
- divisores que recuerden placas base;
- loading states con piezas encajando;
- pequeñas geometrías 3D tipo brick/stud;
- set IDs tratados como códigos de activo financiero.

Evitaremos:

- fondos llenos de piezas;
- ilustraciones cartoon;
- demasiados colores primarios juntos;
- tipografías juguetonas;
- muñecos/minifiguras como decoración principal.

## 3D

Sí usaremos 3D, pero solo donde aporte identidad.

Primera propuesta:

### Hero / Market Overview

Una escena 3D sobria:

- brick negro o amarillo flotando;
- material tipo plástico premium;
- luz suave de estudio;
- rotación lenta;
- studs visibles;
- fondo oscuro o marfil;
- no ocupará toda la interfaz;
- no debe distraer de los KPIs.

Alternativas futuras:

- Set Intelligence: mini objeto 3D del set o brick abstracto;
- Portfolio: pila de bricks como representación de valor acumulado;
- Loading: studs encajando de forma muy sutil.

Regla:

Si el 3D baja rendimiento, ensucia la lectura o parece gimmick, se reduce.

## Pantallas prioritarias de primera UI

Primera versión frontend:

1. **Market Overview**
   - KPIs principales;
   - trend badge;
   - portfolio summary;
   - últimos movimientos;
   - briefing destacado;
   - escena 3D controlada.

2. **Analyze**
   - input URL;
   - resultado con score;
   - market context;
   - anomaly score;
   - margen neto.

3. **Portfolio**
   - posiciones;
   - P&L;
   - señal hold/sell;
   - mejor/peor posición.

Segunda tanda:

4. **Briefings**
5. **Set Intelligence**
6. **Opportunity Scanner**

## Componentes base

- `Shell`
- `Sidebar`
- `TopBar`
- `KpiCard`
- `ScoreBadge`
- `MarketTrendBadge`
- `MarginPill`
- `AnomalyBadge`
- `PortfolioPositionRow`
- `BriefingCard`
- `BrickScene3D`
- `PriceSparkline`
- `ConfidenceDot`

## Tipografía

Dirección:

- sans moderna, limpia, premium;
- números tabulares para precios y KPIs;
- tamaños grandes solo para métricas importantes;
- labels pequeños, uppercase controlado.

Evitar:

- display enorme en cards pequeñas;
- letter spacing negativo;
- textos que parezcan marketing vacío.

## Layout

Desktop-first, responsive.

Estructura:

- sidebar izquierda;
- contenido principal con max-width controlado;
- grid denso pero respirado;
- cards de radio pequeño;
- tablas con mucho cuidado visual;
- detalles LEGO como acento, no como marco completo.

## Regla de oro

La UI debe decir:

> Esto es LEGO, pero visto como mercado, colección y activo.

No:

> Esto es una página de juguetes.
