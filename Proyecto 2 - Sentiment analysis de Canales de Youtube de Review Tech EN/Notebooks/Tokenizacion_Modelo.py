import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# se carga el modelo y el tokenizador
modelo = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
tokenizador = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# funcion para analizar una oracion
def analizar_sentimiento(oracion):
    inputs = tokenizador(oracion, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = modelo(**inputs)
    logits = outputs.logits
    probabilidades = torch.softmax(logits, dim=1).tolist()[0]
    return probabilidades  #[negativo, neutral, positivo]

# funcion para procesar los archivos en el directorio y guardar resultados
def procesar_archivos_en_directorio(directorio_origen, directorio_resultados):
    for carpeta in os.listdir(directorio_origen):
        ruta_carpeta = os.path.join(directorio_origen, carpeta)
        if os.path.isdir(ruta_carpeta):  # verifica si es una carpeta
            carpeta_resultados = os.path.join(directorio_resultados, carpeta)
            os.makedirs(carpeta_resultados, exist_ok=True)  # crear carpeta de resultados si no existe
            
            for archivo in os.listdir(ruta_carpeta):
                if archivo.endswith(".txt"):
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    with open(ruta_archivo, 'r', encoding='utf-8') as file:
                        lineas = file.readlines()

                    resultados = []
                    for oracion in lineas:
                        oracion = oracion.strip()  # se elimina saltos de linea
                        if oracion:  # solo analizar oraciones no vacias
                            probabilidades = analizar_sentimiento(oracion)
                            resultados.append(probabilidades)
                    
                    # se guarda solo los resultados en un archivo de salida
                    ruta_salida = os.path.join(carpeta_resultados, archivo)
                    with open(ruta_salida, 'w', encoding='utf-8') as f:
                        for prob in resultados:
                            f.write(f"{prob}\n")
                    
                    print(f"Análisis completado para el archivo: {ruta_archivo}")

# directorios
directorio_origen = "Data/Preparada"
directorio_resultados = "Data/Resultados"

procesar_archivos_en_directorio(directorio_origen, directorio_resultados)

