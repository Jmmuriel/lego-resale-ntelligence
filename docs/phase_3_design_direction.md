# Fase 3 - Dirección visual premium

Fecha: 2026-05-10

## Visión de diseño

LEGO Resale Intelligence debe sentirse como una herramienta de inteligencia para coleccionistas serios: sobria, precisa, editorial y con un punto de objeto de colección.

La interfaz no debe parecer infantil ni una demo de Streamlit. Debe mezclar:

- claridad de una herramienta financiera;
- sensibilidad de museo / archivo de colección;
- acentos visuales inspirados en LEGO sin copiar literalmente su identidad;
- sensación de producto digital premium.

## Principios

1. Claridad antes que ornamentación.
2. Jerarquía tipográfica fuerte.
3. Espacio en blanco como material de diseño.
4. Rojo LEGO usado como acento, no como fondo dominante.
5. Datos tratados como piezas de colección.
6. Profundidad ligera, sin exceso de sombras.
7. Estados GREEN / YELLOW / RED claros pero sofisticados.
8. Streamlit customizado, no reescrito.
9. Sin features fuera de fase.
10. Cada detalle visual debe ayudar a confiar en el análisis.

## Sistema visual

### Paleta

- Fondo principal: `#f4f1ea`
- Superficie: `#fffdf8`
- Tinta principal: `#171717`
- Texto secundario: `#6f6a61`
- Línea sutil: `rgba(23, 23, 23, 0.12)`
- Rojo acento: `#b91c1c`
- Amarillo oportunidad media: `#d6a900`
- Verde oportunidad alta: `#116b4f`

### Forma

- Radios contenidos: 6-8px.
- Bordes finos y visibles.
- Sombras suaves y controladas.
- Componentes con hover discreto.

### Tipografía

Se usa la tipografía del sistema para mantenerlo ligero en Streamlit.

Jerarquía:

- título principal grande y editorial;
- labels en mayúsculas pequeñas;
- métricas con peso fuerte;
- tablas limpias y compactas.

## Layout de Fase 3

La iteración Fase 3A implementa tres secciones dentro de Streamlit:

1. `Overview`: landing editorial premium con sensación museo + intelligence tool.
2. `Analyze`: sistema operativo de análisis, manteniendo el pipeline de Fase 2.
3. `About`: explicación del método, pipeline, scoring, límites y estado del proyecto.

La sección `Analyze` mantiene:

- panel de entrada de URL;
- resultado con score protagonista;
- grid de métricas clave;
- riesgos detectados;
- breakdown del margen neto;
- tabla de últimos análisis.

## Capa premium aplicada

- Fondo con textura sutil de líneas.
- Objeto pseudo-3D inspirado en un bloque de construcción.
- Score como pieza protagonista.
- Cards de métricas con hover.
- Pills para riesgos.
- Breakdown visual en pasos.
- Tabla con columnas más enfocadas.

## Límites conscientes

Streamlit permite una mejora visual fuerte con CSS, pero no conviene forzar:

- navegación compleja;
- animaciones WebGL;
- transiciones avanzadas entre vistas;
- componentes 3D reales;
- layouts demasiado dependientes de HTML custom.

Para esta fase, el objetivo es una app premium pero mantenible.

## Próximo refinamiento

Revisión visual realizada:

- `Overview` funciona bien como entrada editorial: claro, sobrio y con presencia de producto.
- `Analyze` fue pulido para evitar un panel de input vacío y limpiar la tabla de históricos.
- `About` comunica bien el método y mantiene el tono de sistema transparente.
- Estados `loading`, `error`, `warning`, `success` y `empty` usan paneles visuales propios.
- `Analyze` incluye un inspector simple para revisar un análisis archivado sin cambiar la lógica de negocio.

Siguiente refinamiento:

1. Preparar capturas finales para portfolio.
2. Revisar responsive básico.
3. Si hace falta, añadir una vista de detalle más rica en una iteración posterior.
