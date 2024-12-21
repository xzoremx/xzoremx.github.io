import pandas as pd
import geopandas as gpd

print(gpd.__version__)

# Cargar datos
excel_df = pd.read_csv("Pro1\MTA_Metro_Lines_5653712618533765627.csv")  # Archivo Excel
geo_df = gpd.read_file("Pro1\MTA_Metro_Lines_4952280828455946791.geojson")  # Archivo GeoJSON

# Realizar merge para combinar información
merged_df = geo_df.merge(excel_df, on='NAME')

# Visualizar y guardar
print(merged_df.head())
merged_df.to_file("combined_metro_data.geojson", driver="GeoJSON")

