from googleapiclient.discovery import build
import datetime
import pandas as pd


# API key y el ID de un solo canal
llave_api = "LLAVE_API"
canales_id = [
    "UCBJycsmduvYEL83R_U4JriQ",  # 1. Marques Brownlee
    "UCMiJRAwDNSNzuYeN2uWa0pA",  # 2. Mrwhosetheboss
    "UCXuqSBlHAE6Xw-yeJA0Tunw",  # 3. Linus Tech Tips
    "UCdBK94H6oZT2Q7l0-b0xmMg",  # 4. ShortCircuit
    "UCVYamHliCI9rw1tHR1xbkfw",  # 5. Dave2D
]

youtube = build('youtube', 'v3', developerKey=llave_api)


def obtener_data(youtube, canales_id):
      # Inicializar lista para almacenar los datos
    all_data = []
    
    # Realizar la solicitud a la API de YouTube
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(canales_id)
    )
    response = request.execute()
      
    # Recorrer la respuesta para extraer la informacion relevante (Playlist ID)
    for i in range(len(response['items'])):
        data = {
            'nombre_canal': response['items'][i]['snippet']['title'],
            'numero_subs': response['items'][i]['statistics']['subscriberCount'],
            'numero_vistas': response['items'][i]['statistics']['viewCount'],
            'cantidad_videos': response['items'][i]['statistics']['videoCount'],
            'playlist_id': response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)

    return all_data

print(obtener_data(youtube, canales_id))

#Funcion de obtener los ids de los videos:

canales_data = pd.DataFrame(obtener_data(youtube, canales_id))
print(canales_data)


playlist_id_1 = canales_data.loc[canales_data['nombre_canal'] == 'Marques Brownlee', 'playlist_id'].iloc[0]
playlist_id_2 = canales_data.loc[canales_data['nombre_canal'] == 'Mrwhosetheboss', 'playlist_id'].iloc[0]
playlist_id_3 = canales_data.loc[canales_data['nombre_canal'] == 'Linus Tech Tips', 'playlist_id'].iloc[0]
playlist_id_4 = canales_data.loc[canales_data['nombre_canal'] == 'ShortCircuit', 'playlist_id'].iloc[0]
playlist_id_5 = canales_data.loc[canales_data['nombre_canal'] == 'Dave2D', 'playlist_id'].iloc[0]


def obtener_id_videos_2024(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails,snippet',  # Agregar 'snippet' para obtener detalles de la fecha de publicación
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    videos_id_2024 = []

    for item in response['items']:
        # Obtener la fecha de publicación
        published_at = item['snippet']['publishedAt']
        year = published_at[:4]  # Extraer el año de la fecha

        # Filtrar solo los videos subidos en 2024
        if year == '2024':
            videos_id_2024.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    mas_paginas = True

    while mas_paginas:
        if next_page_token is None:
            mas_paginas = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails,snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                # Obtener la fecha de publicación
                published_at = item['snippet']['publishedAt']
                year = published_at[:4]  # Extraer el año de la fecha

                # Filtrar solo los videos subidos en 2024
                if year == '2024':
                    videos_id_2024.append(item['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return videos_id_2024


# Función para guardar en un archivo .txt
def guardar_en_txt(filename, videos_id):
    with open(filename, 'w') as file:
        for video_id in videos_id:
            file.write(f"{video_id}\n")

# Obtener y guardar los IDs de videos
videos_id_1 = obtener_id_videos_2024(youtube, playlist_id_1)
guardar_en_txt("Data/Sin Procesar/videos_id_MKBHD_2024.txt", videos_id_1)

videos_id_2 = obtener_id_videos_2024(youtube, playlist_id_2)
guardar_en_txt("Data/Sin Procesar/videos_id_MWB_2024.txt", videos_id_2)

videos_id_3 = obtener_id_videos_2024(youtube, playlist_id_3)
guardar_en_txt("Data/Sin Procesar/videos_id_LinusTT_2024.txt", videos_id_3)

videos_id_4 = obtener_id_videos_2024(youtube, playlist_id_4)
guardar_en_txt("Data/Sin Procesar/videos_id_ShortCircuit_2024.txt", videos_id_4)

videos_id_5 = obtener_id_videos_2024(youtube, playlist_id_5)
guardar_en_txt("Data/Sin Procesar/videos_id_Dave2D_2024.txt", videos_id_5)
