import os

# directorio donde se encuentran los archivos .txt
directorio = "Data/Preparada" 

# funcion para combinar las filas hasta que lleguen a una longitud maxima de 512 caracteres
def combinar_filas_en_oraciones(ruta_archivo, max_longitud=512):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        lineas = file.readlines()

    oraciones = []
    oracion_actual = ""

    for linea in lineas:
        # eliminar espacios adicionales y saltos de linea
        linea = linea.strip()

        # si añadir la linea actual excede el límite de 512 caracteres, guarda la oración actual y empieza una nueva
        if len(oracion_actual) + len(linea) + 1 > max_longitud:
            if oracion_actual:
                oraciones.append(oracion_actual)
            oracion_actual = linea
        else:
            # si no excede el limite, añadir la linea a la oración actual
            if oracion_actual:
                oracion_actual += " " + linea
            else:
                oracion_actual = linea

    # añadir la ultima oracion si queda algo pendiente
    if oracion_actual:
        oraciones.append(oracion_actual)

    return oraciones

# funcion para procesar los archivos en el directorio y sobreescribirlos
def procesar_archivos_en_directorio(directorio):
    for carpeta in os.listdir(directorio):
        ruta_carpeta = os.path.join(directorio, carpeta)
        if os.path.isdir(ruta_carpeta):  # Verifica si es una carpeta
            for archivo in os.listdir(ruta_carpeta):
                if archivo.endswith(".txt"):
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    print(f"Procesando archivo: {ruta_archivo}") 
                    oraciones = combinar_filas_en_oraciones(ruta_archivo)

                    # se sobreescribe el archivo con las nuevas oraciones
                    with open(ruta_archivo, 'w', encoding='utf-8') as file:
                        for oracion in oraciones:
                            file.write(oracion + "\n")

                    print(f"Archivo sobreescrito: {ruta_archivo}")

procesar_archivos_en_directorio(directorio)
