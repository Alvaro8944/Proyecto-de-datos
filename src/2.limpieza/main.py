import limpieza
import pandas as pd
import numpy as np

##IMPORTANTE: Antes de ejecutar el codigo, asegurarse de que la linea 12 contiene tu ruta local de archivo_info.txt
## y que la linea 107 tambien tenga una ruta local donde guardar los archivos de salida.

#Descargar el archivo de los datos raw desde drive
urls = []

#Reemplazar el valor de ruta con el directorio local donde se encuentre archivo_info
ruta = "E:/UniversidadCoding/Segundo/Datos PD/archivo_info.txt"

#Procesar el archivo_info.txt y guardar su informacion en la variable archivo_info
archivo_info = limpieza.procesar_archivo_info(ruta)

#Recorremos el archivo info linea por linea (info) y guardamos la ruta donde queda el archivo de cada linea en urls
for info in archivo_info:
    archivo_destino, ruta_completa = limpieza.descargar_archivo_directo(info[0], info[2],
                                                                        info[1])
    urls.append(ruta_completa)
    print(f"Archivo descargado: {archivo_destino}, Ruta: {ruta_completa}")

#A partir de aqui tenemos en urls los 5 archivos que necesitaremos leer para realizar la limpieza de datos.

# Lee el archivo CSV y almacena su contenido en un DataFrame
datos = pd.read_csv(urls[0],usecols = lambda columna: columna!= "Unnamed: 0")

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

## Analizar la descripción
dataframe_descripcion = datos["Descripción"].apply(limpieza.analizar_descripcion)
columnas =["Ascensor","Dormitorios","Num_baños","Año_de_construccion"]
dataframe_descripcion = pd.DataFrame(dataframe_descripcion.tolist(), columns = columnas)
for columna in columnas[1:]:
    datos[columna] = datos[columna].fillna(dataframe_descripcion[columna])
datos["Ascensor"] = datos["Ascensor"].combine(dataframe_descripcion["Ascensor"],max)
datos.loc[datos["Etiqueta"].isna(),"Etiqueta"] = "En proceso"


# Obtener el distrito de la vivienda
urls2 = [urls[1],urls[2]]
datos= limpieza.transformar_localizacion(datos,urls2)

# Nos quedamos solo con los viviendas de tipo "casa","piso"y "ático
viviendas = ["casa","piso","atico"]
filtro_viviendas = datos["Tipo"].isin(viviendas)
datos_viviendas = datos[filtro_viviendas]

#obtener cordenadas
##dataframe_cord = datos_viviendas["distrito/ciudad"].apply(limpieza.get_coords)
##cordenadas_aux = datos_viviendas["Localización"].apply(limpieza.get_coords)
dataframe_cord = pd.read_csv(urls[3],usecols = lambda columna: columna!= "Unnamed: 0")
cordenadas_aux = pd.read_csv(urls[4],usecols = lambda columna: columna!= "Unnamed: 0")
datos_viviendas = datos_viviendas.reset_index(drop = True)
datos_viviendas = pd.concat([datos_viviendas,dataframe_cord],axis =1)
datos_viviendas["Latitud"] = datos_viviendas["Latitud"].fillna(cordenadas_aux["Latitud"])
datos_viviendas["Longitude"] = datos_viviendas["Longitude"].fillna(cordenadas_aux["Longitude"])

#Se debe dejar una de las 2 formas comentada. Se puede ejecutar para cada una de las 2 versiones. Sin embargo
# se debe modificar el nombre del archivo en la linea 107 en funcion de que version estemos obteniendo.

"""
## Forma 1 Elimando las filas con NaN

datos_viviendas.dropna(subset=["Tipo_de_inmueble","Num_baños","Dormitorios","Año_de_construccion"], inplace=True)

"""

# Forma 2 Imputación de valores

# Imputamos los valores NaN de los campos "dormitorios", "num_baños" y "Año de construccion" mediante regresiones
limpieza.imputar_valores(['Precio', 'Superficie'],'Dormitorios',datos_viviendas)
datos_viviendas["Dormitorios"] = datos_viviendas["Dormitorios"].round().astype(int)
limpieza.imputar_valores(['Precio', 'Superficie'],'Num_baños',datos_viviendas)
datos_viviendas["Num_baños"] = datos_viviendas["Num_baños"].round().astype(int)
limpieza.imputar_valores(['Dormitorios', 'Superficie',"Num_baños","Precio"],'Año_de_construccion',datos_viviendas)
datos_viviendas["Año_de_construccion"] = datos_viviendas["Año_de_construccion"].round().astype(int)

# Elimanos la variable planta debido a su gran número de Nulos y la variable localización porque es redundante con distrito
datos_viviendas.dropna(subset=["Tipo_de_inmueble"], inplace=True)
datos_viviendas.drop(["Planta","Localización"], axis=1, inplace=True)

# Finalmente guardamos el fichero. Se debe modificar la ruta local y el nombre del fichero en funcion cual version estemos obteniendo,
# la forma 1 (preprocesado1.parquet) o la forma 2 (preprocesado2.parquet).

#datos_viviendas.to_csv("E:/UniversidadCoding/Segundo/resultados.csv")
datos_viviendas.to_parquet("E:/UniversidadCoding/Segundo/preprocesado2.parquet", engine='pyarrow')









