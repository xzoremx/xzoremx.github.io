import pandas as pd
import os

# ruta donde estan los CSV
dashboard_path = "Dashboards"


# Crear un dataframe vacio para combinar todos los datos
Analisis_Sentimiento_DF = pd.DataFrame()

# Recorrer todas las carpetas y archivos CSV
for channel_folder in os.listdir(dashboard_path):
    channel_folder_path = os.path.join(dashboard_path, channel_folder)
    if os.path.isdir(channel_folder_path):
        for file in os.listdir(channel_folder_path):
            if file.endswith("_sentiment.csv"):
                file_path = os.path.join(channel_folder_path, file)
                # Cargar el CSV
                df = pd.read_csv(file_path)
                # Agregar el DataFrame cargado al conjunto de datos global
                Analisis_Sentimiento_DF = pd.concat([Analisis_Sentimiento_DF, df], ignore_index=True)

# Ver los primeros registros
print(Analisis_Sentimiento_DF.head())

# Guardar el DataFrame combinado en un archivo CSV
output_file_path = "Dashboards/Analisis_Sentimiento_Combinado.csv"
Analisis_Sentimiento_DF.to_csv(output_file_path, index=False)