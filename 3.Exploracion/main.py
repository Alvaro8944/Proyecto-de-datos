import exploracion
import pandas as pd

##Cambiar url con ruta local de los datos preprocesados

##Utilizar el fichero que contiene todas las filas, es decir, el que hemos logrado
##imputando vaores.

url = "/Users/hamzatriki/2ªProyectoDeDatos/preprocesado2.parquet"
datos = pd.read_parquet(url)

print(datos.describe())

# Creamos un nuevo df que tendra solo las columnas numericas
df_drop = exploracion.drop_cualitativas(datos)

# A partir de aqui se utilizara el dataframe "datos" que contiene todas las columnas
# y el dataframe "df_drop" que solo contiene columnas numericas, dependiendo del estudio que
# se realice.

#Vemos las correlaciones en este dataframe. Parece que no son tal altas como esperabamos
#pero se puede deber a que la localización es muy importante y aun no estamos utilizandola.
exploracion.correlacion(df_drop)

#Ahora vemos los boxplots de todas las columnas numericas
exploracion.boxplots(df_drop)

# Pasamos ahora a ver que datos producen los outliers de las coordenadas.
# Nos damos cuenta que los distritos/ciudad "Comillas", "Rio" y "Alcorcón" tienen sus coordenadas
# mal, esto es porque la libreria que se encarga de ello esta buscando otros lugares en vez
# de los distritos de madrid. Visto esto tenemos que solucionarlos a mano en "limpieza.py" (lo solucionaremos en la
# siguiente version por falta de tiempo).
exploracion.revisar_coordenadas(datos)

#Mostramos histogramas para todas las variables númericas
exploracion.histogramas(datos)

#Mostramos gráficas de puntos (scatter)
exploracion.graf_puntos(datos)

#Mostramos una grafica de barras para ver la distribución de propiedades por Tipo y Etiqueta (scatter)
exploracion.barras_tipo_etiqueta(datos)

#Mostramos un mapa creado con las coordenadas de cada inmueble.
mapa = exploracion.crear_mapa(datos)
mapa

