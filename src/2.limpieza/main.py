import limpieza
import pandas as pd
import numpy as np
import requests
import os

#Descargar el archivo de los datos raw desde drive

ruta = "E:/UniversidadCoding/Segundo/Datos PD/archivo_info.txt"
#Guardar en ruta el directorio de archivo_info.txt

archivo_info = limpieza.procesar_archivo_info(ruta)

print(archivo_info)

archivo_destino, ruta_completa = limpieza.descargar_archivo_directo(archivo_info[0][0],archivo_info[0][2],archivo_info[0][1])

#print(archivo_destino,ruta_completa)


# Lee el archivo CSV y almacena su contenido en un DataFrame
url = '/Users/hamzatriki/DatosCasas'
datos = pd.read_csv(url,usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
print(datos.head())

# Aplicamos la función string_to_int() a las columnas "Dormitorios","Superficie","Num_baños" en enteros
ColumnasModificar = ["Dormitorios","Superficie","Num_baños"]
for columna in ColumnasModificar:
    datos[columna] = datos[columna].replace("No disponible",np.nan)
    datos[columna] = datos[columna].apply(limpieza.string_to_int)
# Obtenemos el tipo de casa a partir del enlace y eliminamos la columna Enlace
datos["Tipo"] = datos["Enlace"].apply(limpieza.obtener_tipo_casa)
datos = datos.drop(columns = ["Enlace"])

datos["Precio"] = datos["Precio"].apply(limpieza.string_to_price)
## transformar las variables [Calefaccion","Ascensor","Aire acondicionado","Jardin"] en dicotómicas
datos = limpieza.transformar_en_dicotomicas(datos)
## analizar la descripción
dataframe_descripcion = datos["Descripción"].apply(limpieza.analizar_descripcion)
columnas =["Ascensor","Dormitorios","Num_baños","Año_de_construccion"]
dataframe_descripcion = pd.DataFrame(dataframe_descripcion.tolist(), columns = columnas)
for columna in columnas[1:]:
    datos[columna] = datos[columna].fillna(dataframe_descripcion[columna])
datos["Ascensor"] = datos["Ascensor"].combine(dataframe_descripcion["Ascensor"],max)
datos.loc[datos["Etiqueta"].isna(),"Etiqueta"] = "En proceso"

# obtener el distrito de la vivienda
urls = ["/Users/hamzatriki/Downloads/barrios_municipio_madrid.csv","/Users/hamzatriki/Downloads/municipio_comunidad_madrid.csv"]
datos= limpieza.transformar_localizacion(datos,urls)
# Nos quedamos solo con los viviendas de tipo "casa","piso"y "ático
viviendas = ["casa","piso","atico"]
filtro_viviendas = datos["Tipo"].isin(viviendas)
datos_viviendas = datos[filtro_viviendas]
datos_viviendas.info()

#obtener cordenadas
##dataframe_cord = datos_viviendas["distrito/ciudad"].apply(limpieza.get_coords)
##cordenadas_aux = datos_viviendas["Localización"].apply(limpieza.get_coords)
dataframe_cord = pd.read_csv("/Users/hamzatriki/Downloads/Cordenadas1",usecols = lambda columna: columna!= "Unnamed: 0")
cordenadas_aux = pd.read_csv("/Users/hamzatriki/Downloads/Cordenadas2",usecols = lambda columna: columna!= "Unnamed: 0")
datos_viviendas = datos_viviendas.reset_index(drop = True)
datos_viviendas = pd.concat([datos_viviendas,dataframe_cord],axis =1)
datos_viviendas["Latitud"] = datos_viviendas["Latitud"].fillna(cordenadas_aux["Latitud"])
datos_viviendas["Longitude"] = datos_viviendas["Longitude"].fillna(cordenadas_aux["Longitude"])
print(dataframe_cord)


## Forma 1 Elimando las filas con NaN

datos_viviendas.dropna(subset=["Tipo_de_inmueble","Num_baños","Dormitorios","Año_de_construccion"], inplace=True)


## Forma 2 Imputación de valores

## variables num_dormitorios
limpieza.imputar_valores(['Precio', 'Superficie'],'Dormitorios',datos_viviendas)
datos_viviendas["Dormitorios"] = datos_viviendas["Dormitorios"].round().astype(int)
limpieza.imputar_valores(['Precio', 'Superficie'],'Num_baños',datos_viviendas)
datos_viviendas["Num_baños"] = datos_viviendas["Num_baños"].round().astype(int)
limpieza.imputar_valores(['Dormitorios', 'Superficie',"Num_baños","Precio"],'Año_de_construccion',datos_viviendas)
datos_viviendas["Año_de_construccion"] = datos_viviendas["Año_de_construccion"].round().astype(int)
print(datos_viviendas.info())

## elimanos la variable planta debido a su gran número de Nulos y la variable localización porque es redundante con distrito
datos_viviendas.dropna(subset=["Tipo_de_inmueble"], inplace=True)
datos_viviendas.drop(["Planta","Localización"], axis=1, inplace=True)
print(datos_viviendas.info())
datos_viviendas.to_csv("/Users/hamzatriki/2ªProyectoDeDatos/DatosProcesadosConImputacion")











