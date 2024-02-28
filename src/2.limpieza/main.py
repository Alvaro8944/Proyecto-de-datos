import limpieza
import pandas as pd
import numpy as np

# Lee el archivo CSV y almacena su contenido en un DataFrame
url = '/Users/hamzatriki/Casas_todas'
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

datos = limpieza.transformar_en_dicotomicas(datos)
"""
dataframe_descripcion = datos["Descripción"].apply(limpieza.analizar_descripcion())
columnas =["Ascensor", "Dormitorios","Num_baños"]
dataframe_descripcion = pd.DataFrame(dataframe_descripcion.tolist(), columns = columnas)
for columna in columnas[1:]:
    datos[columna] = datos[columna].fillna(dataframe_descripcion[columna])
datos["Ascensor"] = datos["Ascensor"].combine(dataframe_descripcion["Ascensor"],max)
#urls = []
#limpieza.transformar_localizacion(datos,urls)
"""
print(datos)



