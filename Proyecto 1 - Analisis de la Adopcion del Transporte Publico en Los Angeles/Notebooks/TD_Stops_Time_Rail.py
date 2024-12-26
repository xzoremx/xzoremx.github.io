import pandas as pd

# Cargar el archivo de Excel
archivo_excel = 'Data/Procesada/gtfs_rail/stop_times_clean.xlsx'

# Leer la hoja con la tabla dinámica (puedes especificar el nombre de la hoja)
df = pd.read_excel(archivo_excel, sheet_name='Dist. Viajes según Destino(E)')

# Eliminar las dos primeras filas
df = df.drop([0, 1])

# Definir los nombres de las columnas correctamente
df.columns = ['Station', 'Trip_Percentage']

# Exportar el DataFrame a CSV
df.to_csv('Data/Resultados/TD_stops_times_rail.csv', index=False)


