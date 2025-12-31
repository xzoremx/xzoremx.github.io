from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib


llave_api = "LLAVE_API"

#Se prueba obtener data basica con el canal del Youtuber "Michael Reeves"
canal_id = "UCtHaxi4GTYDpJgMSGy7AeSw"

youtube = build('youtube', 'v3', developerKey=llave_api)

#Funcion para obtener data de un canal

def obtener_data(youtube, canal_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=canal_id)
    response = request.execute()

    data_canal = dict(nombre_canal = response['items'][0]['snippet']['title'],
                      numero_subs = response['items'][0]['statistics']['subscriberCount'],
                      numero_vistas = response['items'][0]['statistics']['viewCount'],
                      cantidad_videos = response['items'][0]['statistics']['videoCount'])

    return data_canal

print(obtener_data(youtube, canal_id))

##################################################################################################

#Considerando los 5 canales de Review Tech de habla inglesa seleccionados
#1. Marques Bronwlee
#2. Mrwhosetheboss
#3. Linus Tech Tips
#4. ShortCircuit
#5. Dave2D

#Se busca comprobar que al menos uno de los canales seleccionados
#se encuentre en la cima de la categoria "Science & Technology" de Youtube

####################################################################################################

regiones_habla_inglesa = ["US", "GB", "CA", "AU", "NZ"]  


def obtener_videos_populares_multi_region(youtube, regiones, categoria_id="28", max_results=50):
    videos = []
    for region in regiones:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region,
            videoCategoryId=categoria_id,
            maxResults=max_results
        )
        response = request.execute()
        
        for item in response['items']:
            videos.append({
                'region': region,
                'video_id': item['id'],
                'titulo_video': item['snippet']['title'],
                'canal_id': item['snippet']['channelId'],
                'nombre_canal': item['snippet']['channelTitle'],
                'vistas': item['statistics'].get('viewCount', 0)
            })
    return pd.DataFrame(videos)


def obtener_detalles_canales(youtube, canales_ids):
    canales_data = []
    for canal_id in canales_ids:
        detalles = obtener_data(youtube, canal_id)  
        canales_data.append(detalles)
    return pd.DataFrame(canales_data)


# Obtener videos populares de regiones de habla inglesa
df_videos_populares = obtener_videos_populares_multi_region(youtube, regiones_habla_inglesa)
print(df_videos_populares)

# Extraer canales unicos de todas las regiones
canales_unicos = df_videos_populares['canal_id'].unique()

# Obtener detalles de los canales
df_canales = obtener_detalles_canales(youtube, canales_unicos)

# Convertir subscriptores a numerico y ordenar
df_canales['numero_subs'] = df_canales['numero_subs'].astype(int)
top_canales = df_canales.sort_values(by='numero_subs', ascending=False).head(7)

print(top_canales)

#Se denota que 3 de los canales elegidos estan en el top 7 de categoria de "Science & Technology" 
#Los 2 primeros del top y el sexto presentan un error de categorizacion por Youtube (son canales de comedia o gaming)