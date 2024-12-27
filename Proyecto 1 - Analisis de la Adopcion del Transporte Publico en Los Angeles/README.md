# Análisis de la Adopción del Transporte Público en Los Ángeles

Este proyecto analiza el uso del transporte público en Los Ángeles, con un enfoque en la relación entre las ubicaciones geográficas de las estaciones de metro y las personas que tienen un tiempo de traslado al trabajo superior a los 90 minutos. A través de un mapa interactivo y un análisis de densidad poblacional, este estudio intenta comprender los factores que afectan la adopción del transporte público, como la accesibilidad de las estaciones, la seguridad en las áreas cercanas y las características sociodemográficas de la población.

## Objetivos

- Analizar la relación entre las ubicaciones geográficas de las estaciones de metro y las personas con tiempos de traslado superiores a 90 minutos.
- Evaluar cómo la distribución de las estaciones y la densidad poblacional impactan el uso del transporte público en Los Ángeles.
- Identificar las estaciones más populares y examinar las posibles causas del bajo uso de algunas estaciones, como la inseguridad y la concentración de personas sin hogar en ciertas áreas.

## Datos Utilizados

- **Estaciones de Metro de Los Ángeles:** Datos geográficos y de rutas de las estaciones de metro y trenes.
- **Población con tiempos de traslado superiores a 90 minutos:** Datos demográficos que incluyen la ubicación de las personas con largos tiempos de traslado al trabajo.
- **Datos de personas sin hogar en Los Ángeles (2024):** Información sobre la población de personas sin hogar en las diferentes áreas de Los Ángeles (SPA).
- **Densidad poblacional de Los Ángeles:** Datos sobre la distribución de la población en las distintas zonas de la ciudad.

## Análisis y Resultados

1. **Mapa Interactivo:** Se creó un mapa poligonal en todo Los Ángeles para comparar la ubicación de las estaciones del metro con las áreas de mayor concentración de personas cuyo tiempo de traslado es superior a 90 minutos. Se observó que las personas con largos tiempos de traslado están ubicadas principalmente en el norte de Los Ángeles (Santa Clarita, Palmdale, Lancaster), donde el sistema de trenes no llega.

2. **Estaciones Populares:** Las estaciones con mayor porcentaje de destino son:
   - **APUS Citrus College Station (18.49%)**
   - **Downtown Long Beach Station (19.16%)**
   - **Downtown Santa Monica Station (10.05%)**
   
   Por otro lado, **Union Station** tiene solo un 11.6% de tráfico a pesar de estar en el centro de Los Ángeles, lo que podría deberse a la presencia de altos niveles de inseguridad en la zona y una mayor concentración de personas sin hogar.

3. **Impacto de la Inseguridad:** Las áreas con mayor concentración de personas sin hogar son las más afectadas por la falta de uso del transporte público. Las tres SPA con más personas sin hogar en Los Ángeles en 2024 son:
   - **SPA Metro (Centro de Los Ángeles):** 18,389 personas sin hogar
   - **SPA South:** 13,886 personas sin hogar
   - **SPA San Fernando:** 10,701 personas sin hogar
   
   Las estaciones como Long Beach y Santa Monica, ubicadas en áreas con menos personas sin hogar, muestran un mayor uso.

4. **Densidad Poblacional y Tiempos de Traslado:** Áreas como Santa Clarita, Palmdale, Lancaster, Lake Los Angeles y Calabasas tienen una alta densidad poblacional y un porcentaje significativo de personas cuyo viaje al trabajo dura más de 90 minutos. Esto sugiere que las personas en estas áreas tienen una mayor necesidad de opciones de transporte público, pero debido a la falta de acceso a las estaciones de tren, se ven obligadas a depender de otros medios de transporte.

## Conclusiones

- Las áreas del norte de Los Ángeles (Santa Clarita, Palmdale, Lancaster) están más alejadas de las estaciones de metro, lo que contribuye a tiempos de traslado largos para sus residentes.
- Las estaciones más populares están ubicadas en áreas con menor concentración de personas sin hogar, lo que indica que la seguridad es un factor importante en la adopción del transporte público.
- El análisis de la densidad poblacional muestra que las zonas con más residentes y largos tiempos de traslado al trabajo (como Santa Clarita y Calabasas) necesitan más cobertura de transporte público.
- Las medidas de seguridad, como el aumento de patrullas y la presencia de personas sin hogar en las estaciones, son factores clave que afectan el uso del transporte público en el centro de Los Ángeles.

## Herramientas Utilizadas

- **Python (Pandas, Matplotlib, Folium):** Para análisis de datos, visualización y creación del mapa interactivo.
- **Power BI:** Para la visualización y análisis de datos adicionales.
- **SQL:** Para la obtención de datos de la base de datos de transporte público y otras fuentes.

## Referencias

- [MediaNews Group, Inc. (2024).](https://dailynews.com) Reporte sobre el aumento de la adopción del transporte público en Los Ángeles.

## Mapa Interactivo

Puedes ver el mapa interactivo de Los Ángeles en el siguiente enlace:



[Ver mapa interactivo](https://xzoremx.github.io/Proyecto%201%20-%20Analisis%20de%20la%20Adopcion%20del%20Transporte%20Publico%20en%20Los%20Angeles/Data/Resultados/mapa_interactivo.html)
