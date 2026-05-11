# Fase 3A - Portfolio visual

## Estado

Fase 3A implementada como una primera experiencia premium dentro de Streamlit, manteniendo la arquitectura funcional construida en Fase 2.

## Objetivo de diseño

La interfaz busca sentirse como una herramienta de inteligencia para coleccionismo: sobria, editorial, limpia y con una referencia sutil al universo LEGO sin caer en una estética infantil.

## Alcance implementado

- Sección `Overview` con landing editorial premium.
- Sección `Analyze` conectada al pipeline real: captura, extracción, identificación, scoring y guardado en SQLite.
- Sección `About` con explicación del pipeline, scoring, limitaciones y estado del proyecto.
- Estados visuales para URL vacía, carga, éxito, error y archivo vacío.
- Tabla simple de últimos análisis guardados.
- Vista detalle simple para inspeccionar un análisis archivado.

## Capturas

Las capturas están guardadas en:

- `docs/screenshots/phase3a_overview.png`
- `docs/screenshots/phase3a_analyze.png`
- `docs/screenshots/phase3a_analyze_detail.png`
- `docs/screenshots/phase3a_about.png`

## Decisiones visuales

- Paleta cálida, sobria y editorial para alejarse del dashboard genérico.
- Rojo LEGO usado como acento de marca, no como color dominante.
- Fondos claros, líneas finas, sombra suave y cards con radio controlado.
- Pseudo-3D ligero en el hero para dar memorabilidad sin meter una librería 3D real.
- Componentes operativos simples para mantener Streamlit mantenible.

## Limitaciones actuales

- Streamlit limita el control fino de navegación, animaciones y layout.
- La app aún no está optimizada específicamente para móvil.
- La tabla y el selector de detalle son componentes nativos de Streamlit con styling limitado.
- No hay sistema de diseño extraído a componentes reutilizables fuera de `app/styles.py`.

## Criterio de cierre de Fase 3A

La Fase 3A puede considerarse cerrada cuando:

- la app mantiene el flujo real de Fase 2;
- las tres secciones principales se ven coherentes;
- los estados visuales principales existen;
- hay capturas de portfolio guardadas;
- los tests automatizados siguen pasando.

Estado actual: cumplido.
