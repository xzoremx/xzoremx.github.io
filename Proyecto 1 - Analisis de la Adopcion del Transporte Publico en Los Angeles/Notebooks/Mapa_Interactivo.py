import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import branca.colormap as cm
import geopandas as gpd
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cm
from geopy.distance import geodesic
from difflib import SequenceMatcher
import branca


# Cargar datos desde el archivo Excel
df_homeless = pd.read_excel("Data/Procesada/Poblacion_SinHogar_SPA_Limpia.xlsx")

# Cargar el GeoJSON
spa_geojson = gpd.read_file("Data/Procesada/SPA.geojson")

# Verificar las primeras filas
print(df_homeless.head())
print(spa_geojson.head())

# Transforma los datos Excel de columnas a formato largo
df_homeless_long = df_homeless.melt(id_vars=["Year"], 
                                       var_name="SPA_NUM", 
                                       value_name="Population")

# Quitar "SPA " del nombre para que coincida con los datos del GeoJSON
df_homeless_long["SPA_NUM"] = df_homeless_long["SPA_NUM"].str.replace("SPA ", "").astype(int)

# Verifica la transformación
print(df_homeless_long.head())

# Combina los datos geográficos con los datos de población
data_combinada = spa_geojson.merge(df_homeless_long, on="SPA_NUM")

# Verifica la unión
print(data_combinada.head())

# Filtra los datos para un año específico (por ejemplo, 2024)
year_2024 = data_combinada[data_combinada["Year"] == 2024]

# Creando un mapa
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
year_2024.plot(column="Population", 
               cmap="OrRd", 
               legend=True, 
               ax=ax)
plt.title("Población de Personas Sin Hogar por SPA (2024)", fontsize=16)
# Guardar el gráfico como archivo
plt.savefig("Data/Resultados/Población de Personas Sin Hogar por SPA (2024).png", dpi=300, bbox_inches="tight")
#plt.show()
plt.close() 

# Calcular diferencias de población entre 2024 y 2023
diff_data = data_combinada.pivot(index="SPA_NUM", columns="Year", values="Population")
diff_data["Change_2024_2023"] = diff_data[2024] - diff_data[2023]

# Agregar la diferencia al GeoDataFrame
spa_geojson = spa_geojson.merge(diff_data["Change_2024_2023"], on="SPA_NUM")

# Mapa de diferencias
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
spa_geojson.plot(column="Change_2024_2023", 
                 cmap="RdYlGn", 
                 legend=True, 
                 ax=ax)
plt.title("Cambio en Población Sin Hogar (2024 vs 2023)", fontsize=16)

# Guardar el gráfico como archivo
plt.savefig("Data/Resultados/Cambio en Población Sin Hogar (2024 vs 2023).png", dpi=300, bbox_inches="tight")
#plt.show()
plt.close() 

#######################################################################################################################
# Leer datos
metro_stations = gpd.read_file("Data/Procesada/Metro_Stations.geojson")
TD_Stops_Time_Rail = pd.read_csv('Data/Resultados/TD_stops_times_rail.csv')
LACounty_geojson = gpd.read_file("Data/Procesada/LA_County.geojson")
PopDens_LA_geojson = gpd.read_file("Data/Procesada/PoblacionDensidad_LA.geojson")

# Reproyectar a EPSG:4326
LACounty_geojson = LACounty_geojson.to_crs(epsg=4326)
PopDens_LA_geojson = PopDens_LA_geojson.to_crs(epsg=4326)

#Definicion de Capas
SPA_layer = folium.FeatureGroup(name="SPA - Población Sin Hogar")
LACounty_layer = folium.FeatureGroup(name="Mapa Poligonal: Trabajadores con tiempo de traslado > 90 minutos")
PopDen_LA_layer = folium.FeatureGroup(name="Mapa Poligonal: Densidad Poblacional")
MetroLines_layer = folium.FeatureGroup(name="Lineas de Metro")


# Extraer la columna de población total (B01001_001)
# Asegurémonos de que 'B01001_001' es la columna correcta para la población total
PopDens_LA_geojson['PoblacionTotal'] = PopDens_LA_geojson['B01001_001']



# Obtener los valores mínimo y máximo de población
min_pop = PopDens_LA_geojson['PoblacionTotal'].min()
max_pop = PopDens_LA_geojson['PoblacionTotal'].max()



# Crear un mapa centrado en Los Ángeles
m = folium.Map(location=[34.0522, -118.2437], zoom_start=9, tiles="CartoDB Dark_Matter")

print(PopDens_LA_geojson.head())

# Definir el gradiente de colores para el choropleth
colormap_Pop = branca.colormap.LinearColormap(
    colors=['white', 'purple'],  # Blanco para menos población, lila para más población
    vmin=min_pop, vmax=max_pop,
    caption="Densidad Poblacional (2024)"
).to_step(n=10)  # Usamos un gradiente con 10 pasos
colormap_Pop.add_to(m)


# Crear una capa de choropleth basada en la población
folium.GeoJson(
    PopDens_LA_geojson,
    style_function=lambda feature: {
        'fillColor': colormap_Pop(feature['properties']['PoblacionTotal']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.2
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['GEOID', 'PoblacionTotal'],
        aliases=['GEOID:', 'Población Total:']
    )
).add_to(PopDen_LA_layer)


# Definir una función para asignar colores según los rangos de la columna B08303__35
def get_color(value):
    if value > 6.3:
        return 'red'  # Valores mayores a 6.3%
    elif 2.8 <= value <= 6.3:
        return 'orange'  # Valores entre 2.8% (promedio nacional) y 6.3%
    elif 0.1 <= value < 2.8:
        return 'yellow'  # Valores entre 0.1% y 2.8%
    else:  # value < 0.1
        return 'white'  # Valores menores a 0.1%
    
# Normalizar los valores de población para el gradiente
population = year_2024["Population"]
min_pop, max_pop = population.min(), population.max()

# Crear un mapa de colores (gradiente de blanco a naranja)
colormap = cm.LinearColormap(
    colors=["white", "yellow", "orange"],
    vmin=min_pop,
    vmax=max_pop,
    caption="Población sin hogar (2024)"
)
colormap.add_to(m)

# Añadir polígonos con colores dinámicos
for _, row in year_2024.iterrows():
    color = colormap(row["Population"])
    folium.GeoJson(
        row["geometry"],
        name=row["SPA_NAME"],
        style_function=lambda x, color=color: {
            "fillColor": color,
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.3,
        },
        tooltip=folium.Tooltip(f"""
            <strong>{row['SPA_NAME']}</strong><br>
            Población sin hogar (2024): {row['Population']}
        """),
    ).add_to(SPA_layer)

# Añadir la capa estilizada al mapa
folium.GeoJson(
    LACounty_geojson,
    name="Porcentaje según B08303__35",
    style_function=lambda feature: {
        'fillColor': get_color(feature['properties']['B08303__35']),
        'color': 'black',  # Borde en negro
        'weight': 0.3,
        'fillOpacity': 0.2
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NAME', 'B08303__35'],  # Muestra el nombre y el valor en el tooltip
        aliases=['Área:', 'Porcentaje:'],
        localize=True
    )
).add_to(LACounty_layer)


# Merge para agregar coordenadas a las estaciones de destino
Estaciones_Ubicaciones = TD_Stops_Time_Rail.merge(metro_stations[['Name', 'geometry']], 
                                                  left_on='Station', 
                                                  right_on='Name', 
                                                  how='left')

Estaciones_Ubicaciones['POINT_X'] = Estaciones_Ubicaciones['geometry'].apply(lambda geom: geom.x if geom else None)
Estaciones_Ubicaciones['POINT_Y'] = Estaciones_Ubicaciones['geometry'].apply(lambda geom: geom.y if geom else None)
Estaciones_Ubicaciones = Estaciones_Ubicaciones.dropna(subset=['POINT_X', 'POINT_Y'])

# Filtrar nombres similares
def filter_similar_names(data, threshold=0.9):
    filtered_data = []
    seen = set()

    for idx, row in data.iterrows():
        station_name = row['Station']
        if station_name in seen:
            continue

        similar = [other for other in data['Station'] if SequenceMatcher(None, station_name, other).ratio() > threshold]
        seen.update(similar)
        filtered_data.append(row)

    return pd.DataFrame(filtered_data)

# Aplicar filtro de nombres similares
Estaciones_Ubicaciones = filter_similar_names(Estaciones_Ubicaciones)

# Iterar sobre estaciones destino y agregar marcadores color cyan
for idx, row in Estaciones_Ubicaciones.iterrows():
    radius = row['Trip_Percentage'] * 70  # Ajustar tamaño dinámico
    folium.CircleMarker(
        location=[row['POINT_Y'], row['POINT_X']],
        radius=radius,
        color="cyan",
        fill=True,
        fill_color="cyan",
        fill_opacity=0.6,
        popup=folium.Popup(f"Estación: {row['Station']}<br>Porcentaje de viajes hacia esta estación: {round(row['Trip_Percentage'] * 100, 2)}%", max_width=300)
    ).add_to(m)

# Filtrar duplicados por ubicación
unique_points = []
filtered_stations = []

for idx, row in metro_stations.iterrows():
    point = (row['geometry'].y, row['geometry'].x)
    if any(geodesic(point, unique).meters < 50 for unique in unique_points):  # Umbral de 50m
        continue

    unique_points.append(point)
    filtered_stations.append(row)

filtered_stations = pd.DataFrame(filtered_stations)

# Agregar estaciones no destino en verde
for idx, row in filtered_stations.iterrows():
    if row['Name'] in TD_Stops_Time_Rail['Station'].tolist():  # Omitir destinos
        continue
    
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=1,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.5,
        popup=folium.Popup(f"Estación: {row['Name']}", max_width=300)
    ).add_to(m)

#################################################################################################################################
#################################################################################################################################

#INCLUYENDO LAS LINEAS DE METRO EN EL MAPA

metro_lines = gpd.read_file('Data/Procesada/MTA_Metro_Lines.geojson')

active_lines = metro_lines[(metro_lines['STATUS'] == 'Existing')]


# Añadir las líneas activas al mapa
for _, row in active_lines.iterrows():
    # Definir el color de la línea según el nombre
    line_color = {
        'Blue Line': 'blue',
        'K Line': 'green',
        'Green Line': 'lime',
        'Expo Line': 'purple',
        'Purple Line': 'violet',
        'Red Line': 'red',
        'Gold Line': 'gold'
    }.get(row['NAME'], 'gray')  # Color por defecto si no está en el diccionario

    # Agregar cada línea al mapa
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, color=line_color: {
            'color': color,
            'weight': 4,  # Grosor de la línea
            'opacity': 0.7
        },
        tooltip=row['NAME']  # Mostrar el nombre de la línea en el tooltip
    ).add_to(MetroLines_layer)

##############################################################################################################
##############################################################################################################

# Añadir las capas al mapa
SPA_layer.add_to(m)

LACounty_layer.add_to(m)

PopDen_LA_layer.add_to(m)

MetroLines_layer.add_to(m)



# Añadir control de capas
folium.LayerControl().add_to(m)


# Guardar el mapa
output_path = "Data/Resultados/mapa_interactivo.html"
m.save(output_path)
print(f"Mapa interactivo guardado en {output_path}")