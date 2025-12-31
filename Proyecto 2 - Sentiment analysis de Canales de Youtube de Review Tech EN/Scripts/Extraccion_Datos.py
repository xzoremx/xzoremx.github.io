import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el dataframe desde el archivo CSV
input_file_path = "Dashboards/Analisis_Sentimiento_Combinado.csv"
df = pd.read_csv(input_file_path)


# Verificar que se haya cargado correctamente
print("Primeras filas del DataFrame:")
print(df.head())

# Definir la función de cálculo de sentimiento global
def calcular_sentimiento_global(row):
    # Obtener el sentimiento con mayor valor
    max_sentimiento = row[["Negative", "Neutral", "Positive"]].idxmax()  # Esto devuelve el nombre de la columna con el valor máximo
    return max_sentimiento

# Aplicar la función a todo el DataFrame
df['Sentimiento_Global'] = df.apply(calcular_sentimiento_global, axis=1)

# Calcular el Sentimiento Promedio por Video
sentimiento_promedio_video = df.groupby('Video_ID')[['Negative', 'Neutral', 'Positive']].mean()

# Calcular el Sentimiento Promedio por Canal
sentimiento_promedio_canal = df.groupby('Channel')[['Negative', 'Neutral', 'Positive']].mean()

# Calcular el Sentimiento Global por Canal
sentimiento_global_canal = df.groupby('Channel')['Sentimiento_Global'].agg(lambda x: x.mode()[0])

# Calcular la distribución de sentimientos por canal
sentimiento_distribution = df.groupby('Channel')[['Negative', 'Neutral', 'Positive']].sum()

# Convertir a porcentajes
sentimiento_distribution_percentage = sentimiento_distribution.div(sentimiento_distribution.sum(axis=1), axis=0) * 100

# Calcular el sentimiento global promedio
sentimiento_global = df[['Negative', 'Neutral', 'Positive']].mean()

# Identificar el video con mayor sentimiento negativo
video_mas_negativo = df.loc[df['Negative'].idxmax()]

# Identificar el video con mayor sentimiento positivo
video_mas_positivo = df.loc[df['Positive'].idxmax()]

# Mostrar resultados de los videos con mayor sentimiento
print(f"\nVideo más negativo: {video_mas_negativo['Video_ID']}, Sentimiento negativo: {video_mas_negativo['Negative']}")
print(f"Video más positivo: {video_mas_positivo['Video_ID']}, Sentimiento positivo: {video_mas_positivo['Positive']}")

# Mostrar el sentimiento global promedio
print("\nSentimiento Global Promedio:")
print(sentimiento_global)

# Mostrar el sentimiento promedio por video
print("\nSentimiento Promedio por Video:")
print(sentimiento_promedio_video.head())

# Mostrar la distribución de sentimientos por canal en porcentaje
print("\nDistribución de Sentimientos por Canal (en porcentaje):")
print(sentimiento_distribution_percentage)

# Mostrar el sentimiento promedio por canal
print("\nSentimiento Promedio por Canal:")
print(sentimiento_promedio_canal.head())

# Mostrar el sentimiento global por canal
print("\nSentimiento Global por Canal:")
print(sentimiento_global_canal.head())

# Guardar los resultados en archivos CSV
sentimiento_promedio_video.to_csv("Dashboards/Sentimiento_Promedio_Video.csv")
sentimiento_promedio_canal.to_csv("Dashboards/Sentimiento_Promedio_Canal.csv")
sentimiento_global_canal.to_csv("Dashboards/Sentimiento_Global_Canal.csv")

# Crear un gráfico de barras con los sentimientos promedio por canal
plt.figure(figsize=(10, 6))
sns.barplot(x=sentimiento_promedio_canal.index, y=sentimiento_promedio_canal['Positive'], color='green', label='Positivo')
sns.barplot(x=sentimiento_promedio_canal.index, y=sentimiento_promedio_canal['Negative'], color='red', label='Negativo')

plt.title('Sentimiento Promedio por Canal')
plt.xlabel('Canal')
plt.ylabel('Promedio de Sentimiento')
plt.legend()
plt.xticks(rotation=45)
plt.show()


# Calcular la correlación entre los sentimientos positivos y negativos
correlation = df[['Negative', 'Positive']].corr()


# Mostrar la correlación
print("\nCorrelación entre Sentimientos Negativos y Positivos:")
print(correlation)
