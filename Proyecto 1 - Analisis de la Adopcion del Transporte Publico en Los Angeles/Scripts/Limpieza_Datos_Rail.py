import pandas as pd

# Cargar archivos


routes = pd.read_csv("Data/Sin Procesar/gtfs_rail/routes.txt")
shapes = pd.read_csv("Data/Sin Procesar/gtfs_rail/shapes.txt")
stop_times = pd.read_csv("Data/Sin Procesar/gtfs_rail/stop_times.txt")
stops = pd.read_csv("Data/Sin Procesar/gtfs_rail/stops.txt")
trips = pd.read_csv("Data/Sin Procesar/gtfs_rail/trips.txt")

# Ver las primeras filas para explorar los datos

print(routes.head())
print(shapes.head())
print(stop_times.head())
print(stops.head())
print(trips.head())

# Eliminar las columnas vacías

routes_clean = routes.dropna(axis=1, how='all')
routes_clean.to_csv("Data/Procesada/gtfs_rail/routes_clean.csv", index=False)

shapes_clean = shapes.dropna(axis=1, how='all')
shapes_clean.to_csv("Data/Procesada/gtfs_rail/shapes_clean.csv", index=False)

stop_times_clean = stop_times.dropna(axis=1, how='all')
stop_times_clean.to_csv("Data/Procesada/gtfs_rail/stop_times_clean.csv", index=False)

stops_clean = stops.dropna(axis=1, how='all')
stops_clean.to_csv("Data/Procesada/gtfs_rail/stops_clean.csv", index=False)

trips_clean = trips.dropna(axis=1, how='all')
trips_clean.to_csv("Data/Procesada/gtfs_rail/trips_clean.csv", index=False)