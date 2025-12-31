# Análisis de Sentimientos de Canales de Review Tech en YouTube

Este proyecto analiza los sentimientos expresados en los subtítulos de videos de cinco canales de tecnología en YouTube: **Dave2D**, **Linus Tech Tips**, **Marques Brownlee**, **Mrwhosetheboss**, y **ShortCircuit**. El objetivo principal es examinar el lenguaje utilizado en las reseñas tecnológicas y comparar los patrones de sentimientos entre estos canales.

## Descripción

Este análisis se lleva a cabo utilizando los archivos de subtítulos generados automáticamente por YouTube (archivos CSV), que contienen las transcripciones de los videos. A través de herramientas de análisis de datos como **Python**, **Excel** y **Power BI**, se procesan los datos para extraer los sentimientos de los videos y generar visualizaciones interactivas.


## Objetivo del Proyecto

- **Análisis de Sentimiento:** Evaluar el sentimiento (positivo, negativo y neutral) en los subtítulos de los videos.
- **Comparación de Canales:** Comparar los patrones de sentimientos entre los cinco canales de tecnología seleccionados.
- **Visualización de Resultados:** Crear gráficos y dashboards interactivos para explorar los insights de los sentimientos en los videos.

## Estructura del Proyecto

- `data/`: Carpeta que contiene los archivos CSV con los subtítulos de los videos.
- `scripts/`: Contiene los scripts en Python para procesamiento y análisis de los datos.
- `visualizations/`: Archivos de Power BI con las visualizaciones interactivas de los resultados.
- `resultados_sentimientos.csv`: Archivo exportado con la distribución de sentimientos por canal.

## Herramientas Utilizadas

- **Python**: Para procesamiento de datos y análisis de sentimiento utilizando librerías como `TextBlob`.
- **Excel**: Para limpieza y preparación de los datos antes de su análisis.
- **Power BI**: Para la creación de visualizaciones interactivas de los resultados.

## Insights Clave

### Video más negativo y más positivo

- **Video más negativo**: `bxzcNeAoB5g`, Sentimiento negativo: `0.9800328612327576`
- **Video más positivo**: `nK9zxuXa3OA`, Sentimiento positivo: `0.9923664927482604`

### Sentimiento Global Promedio

- **Negativo**: `0.230164`
- **Neutral**: `0.368077`
- **Positivo**: `0.401759`

### Sentimiento Promedio por Canal

| Canal             | Negativo | Neutral | Positivo |
|-------------------|----------|---------|----------|
| Dave2D            | 0.142319 | 0.316476| 0.541205 |
| Linus Tech Tips   | 0.253702 | 0.386376| 0.359922 |
| Marques Brownlee  | 0.124739 | 0.322889| 0.552372 |
| Mrwhosetheboss    | 0.211886 | 0.317054| 0.471060 |
| ShortCircuit      | 0.151616 | 0.309624| 0.538760 |

### Sentimiento Global por Canal

- **Dave2D**: Positivo
- **Linus Tech Tips**: Neutral
- **Marques Brownlee**: Positivo
- **Mrwhosetheboss**: Positivo
- **ShortCircuit**: Positivo

### Correlación entre Sentimientos Negativos y Positivos

- Correlación: `-0.788863` (Fuerte correlación negativa entre los sentimientos negativos y positivos)




