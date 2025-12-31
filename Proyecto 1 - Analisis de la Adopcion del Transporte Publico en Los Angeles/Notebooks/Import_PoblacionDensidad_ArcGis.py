import geopandas as gpd

# Definir las rutas de entrada y salida

shapefile_path = r"Data/Sin Procesar/ACS Population Variables - Boundaries/population_den.shp"
# Cargar el shapefile en un GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Guardar el GeoDataFrame como GeoJSON
geojson_path = r"Data/Procesada/PoblacionDensidad_LA.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")

print(f"Archivo GeoJSON guardado en: {geojson_path}")