import limpieza
import pandas as pd
import numpy as np
import requests
import os


def descargar_archivo_directo(id_archivo, directorio_destino, archivo_destino):
    """
    Descarga un archivo directamente desde Google Drive y lo guarda localmente.

    Parámetros:
    - id_archivo (str): ID del archivo en Google Drive.
    - directorio_destino (str): Ruta del directorio local donde se guardará el archivo.
    - archivo_destino (str): Nombre deseado para el archivo en local

    Devuelve:
    - archivo_destino (str): Nombre del archivo guardado.
    - ruta_completa (str): Ruta completa del archivo guardado.
    """
    # Construye la URL de descarga directa utilizando el ID del archivo
    url = f"https://drive.google.com/uc?export=download&id={id_archivo}"

    # Realiza la petición HTTP GET para descargar el archivo
    respuesta = requests.get(url, allow_redirects=True)

    # Comprueba que el directorio destino existe, si no, lo crea
    os.makedirs(directorio_destino, exist_ok=True)

    # Construye la ruta completa donde se guardará el archivo en local
    ruta_completa = os.path.join(directorio_destino, archivo_destino)

    # Guarda el contenido del archivo descargado en local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)


    return archivo_destino, ruta_completa

def procesar_archivo_info(ruta_archivo_info):
    """
    Procesa un archivo de texto que contiene información sobre los archivos a descargar.

    Parámetros:
    - ruta_archivo_info (str): Ruta del archivo de texto que contiene los IDs de Google Drive,
                               los nombres de los archivos locales y las rutas locales.

    Devuelve:
    - Una lista de tuplas con el ID de Google Drive, el nombre local del archivo, y la ruta local.
    """
    archivos_info = []
    with open(ruta_archivo_info, 'r') as archivo:
        for linea in archivo:
            id_archivo, nombre_archivo, directorio_destino = linea.strip().split(',')
            archivos_info.append((id_archivo, nombre_archivo, directorio_destino))
    return archivos_info



# Lee el archivo CSV y almacena su contenido en un DataFrame
url = '/Users/hamzatriki/DatosCasas'
datos = pd.read_csv(url,usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
print(datos.head())

ColumnasModificar = ["Dormitorios","Superficie","Num_baños"]
for columna in ColumnasModificar:
    datos[columna] = datos[columna].replace("No disponible",np.nan)
    datos[columna] = datos[columna].apply(limpieza.string_to_int)
datos["Tipo"] = datos["Enlace"].apply(limpieza.obtener_tipo_casa)
datos = datos.drop(columns = ["Enlace"])
datos["Precio"] = datos["Precio"].apply(limpieza.string_to_price)
## transformar las variables [Calefaccion","Ascensor","Aire acondicionado","Jardin"] en dicotómicas
datos = limpieza.transformar_en_dicotomicas(datos)
## analizar la descripción
dataframe_descripcion = datos["Descripción"].apply(limpieza.analizar_descripcion)
columnas =["Ascensor", "Dormitorios","Num_baños","Año_de_construccion"]
dataframe_descripcion = pd.DataFrame(dataframe_descripcion.tolist(), columns = columnas)
for columna in columnas[1:]:
    datos[columna] = datos[columna].fillna(dataframe_descripcion[columna])
datos["Ascensor"] = datos["Ascensor"].combine(dataframe_descripcion["Ascensor"],max)
datos.loc[datos["Etiqueta"].isna(),"Etiqueta"] = "En proceso"

# obtener el distrito de la vivienda
urls = ["/Users/hamzatriki/Downloads/barrios_municipio_madrid.csv","/Users/hamzatriki/Downloads/municipio_comunidad_madrid.csv"]
datos = limpieza.transformar_localizacion(datos,urls)

# Nos quedamos solo con los viviendas de tipo "casa","piso"y "ático
viviendas = ["casa","piso","atico"]
filtro_viviendas = datos["Tipo"].isin(viviendas)
datos_viviendas = datos[filtro_viviendas]
datos_viviendas.info()

#obtener cordenadas
dataframe_cord = datos_viviendas["distrito/ciudad"].apply(limpieza.get_coords)
print(dataframe_cord)







