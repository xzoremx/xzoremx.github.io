import os
import pandas as pd

# Ruta a la carpeta que contiene los resultados
base_path = "Data/Resultados"

base_dashboard_path = "Dashboards"


# Mapeo de las carpetas a los nombres de los canales
channel_mapping = {
    'Dave2D_2024': 'Dave2D',
    'LinusTT_2024': 'Linus Tech Tips',
    'MKBHD_2024': 'Marques Brownlee',
    'MWB_2024': 'Mrwhosetheboss',
    'ShortCircuit_2024': 'ShortCircuit'
}

# Función para leer los archivos .en.txt y extraer los sentimientos
def process_files(channel_folder, channel_name):
    # Ruta de la carpeta del canal
    folder_path = os.path.join(base_path, channel_folder)
    
    # Ruta para guardar los archivos CSV
    save_folder_path = os.path.join(base_dashboard_path, channel_folder)  # Guardar en la misma estructura de carpetas
    
    # Crear la carpeta del canal si no existe
    os.makedirs(save_folder_path, exist_ok=True)
    
    # Recorrer cada archivo en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".en.txt"):  # Asegurarse de leer solo los archivos .en.txt
            file_path = os.path.join(folder_path, filename)
            
            # Extraer el ID del video (eliminando la extensión .en.txt)
            video_id = filename.split('.en.txt')[0]
            
            # Abrir y leer el archivo
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Asumimos que el análisis de sentimiento está en el formato [negativo, neutro, positivo]
            video_results = []
            
            # Procesar cada línea de sentimientos
            for line in lines:
                try:
                    sentiment_values = eval(line.strip())  # Convertir a lista de flotantes
                    result = {
                        'Channel': channel_name,
                        'Video_ID': video_id,
                        'Negative': sentiment_values[0],
                        'Neutral': sentiment_values[1],
                        'Positive': sentiment_values[2]
                    }
                    video_results.append(result)
                except:
                    continue
            
            # Crear un DataFrame para el video
            df_video = pd.DataFrame(video_results)
            
            # Guardar el DataFrame en un archivo CSV individual por video
            save_file_path = os.path.join(save_folder_path, f'{video_id}_sentiment.csv')
            df_video.to_csv(save_file_path, index=False)
            print(f"Datos guardados para video {video_id} en {save_file_path}")

# Procesar los archivos de cada canal
for channel_folder, channel_name in channel_mapping.items():
    process_files(channel_folder, channel_name)