import limpieza
import pandas as pd
import numpy as np

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
limpieza.transformar_localizacion(datos,urls)

# Nos quedamos solo con los viviendas de tipo "casa","piso"y "ático
viviendas = ["casa","piso","atico"]
filtro_viviendas = datos["Tipo"].isin(viviendas)
datos_viviendas = datos[filtro_viviendas]
datos_viviendas.info()





