import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL de la pagina con la tabla
url = "https://www.laalmanac.com/social/so14.php"

# Obtener el HTML de la página
response = requests.get(url)
html_content = response.content

# Usar pandas para extraer tablas directamente
tables = pd.read_html(html_content)

# Seleccionar la segunda tabla
df = tables[1]
print(df.head())
df.to_csv("Data/Sin Procesar/Poblacion_SinHogar_SPA.csv", index=False)