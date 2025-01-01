import os

# ruta al directorio que contiene los archivos .txt con los IDs de los videos
directorio_txt = 'Data\\Sin Procesar\\'

# ruta donde quieres guardar los subtítulos (directorio Procesada)
directorio_destino = 'Data\\Procesada\\'


# Diccionario que mapea los archivos .txt a sus respectivos nombres de canal
canales = {
    'videos_id_MKBHD_2024.txt': 'MKBHD_2024',
    'videos_id_MWB_2024.txt': 'MWB_2024',
    'videos_id_LinusTT_2024.txt': 'LinusTT_2024',
    'videos_id_ShortCircuit_2024.txt': 'ShortCircuit_2024',
    'videos_id_Dave2D_2024.txt': 'Dave2D_2024'
}

# Obtener todos los archivos .txt en el directorio especificado
archivos_txt = [archivo for archivo in os.listdir(directorio_txt) if archivo.endswith('.txt')]

# Procesar cada archivo .txt
for archivo_txt in archivos_txt:
    # Leer los IDs de cada archivo .txt
    with open(os.path.join(directorio_txt, archivo_txt), 'r') as archivo:
        video_ids = archivo.readlines()

    # Obtener el nombre del canal correspondiente
    canal = canales.get(archivo_txt, None)

    if canal:
        # se crea una carpeta para el canal si no existe
        carpeta_canal = os.path.join(directorio_destino, canal)
        if not os.path.exists(carpeta_canal):
            os.makedirs(carpeta_canal)

        # Descargar subtitulos para cada video en el archivo actual
        for video_id in video_ids:
            video_id = video_id.strip()  # eliminar saltos de linea y espacios extra
            url_video = f'https://www.youtube.com/watch?v={video_id}'

            # Ejecutar el comando yt-dlp para descargar subtítulos
            comando = f'yt-dlp --write-auto-subs --skip-download --sub-lang en --sub-format "vtt" --output "{carpeta_canal}\\%(id)s.%(ext)s" {url_video}'

           
            os.system(comando)

            print(f"Subtítulos descargados para el video {video_id} desde {archivo_txt} en la carpeta {canal}")

print("Proceso completado.")



