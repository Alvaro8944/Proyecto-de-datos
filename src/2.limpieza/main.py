import limpieza
import pandas as pd
import numpy as np

# Lee el archivo CSV y almacena su contenido en un DataFrame
url = '//Users//hamzatriki//Downloads//Casas_todas'
datos = pd.read_csv(url,usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
print(datos.head())

ColumnasModificar = ["Dormitorios","Superficie","Num_baños","Precio"]
for columna in ColumnasModificar:
    datos[columna] = datos[columna].replace("No disponible",np.nan)
    datos[columna] = datos[columna].apply(limpieza.string_to_int())
datos["Tipo"] = datos["Enlace"].apply(limpieza.obtener_tipo_casa())
datos = datos.drop(columns = ["Enlace"])



