import numpy as np
import pandas as pd
import re
from time import sleep
from geopy.geocoders import Nominatim
from sklearn.linear_model import LinearRegression
import requests
import os


# Lee el archivo CSV y almacena su contenido en un DataFrame
##datos = pd.read_csv('C:/Users/dalon/Desktop/UCM/2º/PROYECTO_DATOS_I/Casas_todas.csv',usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
##print(datos.head())

#Funciones publicas


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

def string_to_int(x):
    """recibe un string que sigue la siguiente estructura : dígito seguido de una característica (2 dormitorios,3 baños)
    y devuelve el entero
    """
    if not pd.isnull(x):
        x_split = x.split()
        return int(x_split[0])
    else:
        return np.nan

def obtener_tipo_casa(x):
    """ recibe un enlace como el siguiente "https://www.tecnocasa.es/venta/piso/madrid/madrid/523991.html" y devuelve
    que tipo de vivienda es, en este caso /piso/"""
    return x.split("/")[4]

def string_to_price(x):
    """recibe el precio de una casa en formato "25.000 €" elimina el simbolo del euro y devuelve un entero
    representando el precio"""
    return pd.to_numeric(x.split()[0].replace(".",""),errors='coerce')

def string_to_dicotomic(x):
    """Funcion auxiliar,Recibe un objeto, si este es Nan considera que dicha vivienda no dispone de esa característica,
    en caso contrario,si"""
    if not pd.isnull(x):
        return 1
    else:
        return 0

def transformar_en_dicotomicas(datos):
    """Recorre las columnas [Calefaccion","Ascensor","Aire acondicionado","Jardin"] y decide si la vivienda dispone
     de esa característica"""
    columnasDicotomicas = ["Calefaccion","Ascensor","Aire acondicionado","Jardin"]
    for columna in columnasDicotomicas:
        datos[columna] = datos[columna].replace("No disponible",np.nan)
        datos[columna] = datos[columna].apply(string_to_dicotomic)
    return datos

def analizar_descripcion(texto):
    """Recibe un string que representa la descripción de cada vivienda, usamos la descripción para completar nuestros datos
    ya que tenemos algunos nulos en variables como "num_habitaciones" o "num_baños" y podemos sacar esa información de la descripción,
    """
    ascensor = buscar_palabra(texto, "ascensor")
    num_habitaciones = extraer_numero_dormitorios_baños(texto,r'(\b\d+\b|(un(o|a)?|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\b)\s+(dormitorio|habitación)s?')
    num_baños = extraer_numero_dormitorios_baños(texto,r'(\b\d+\b|(un(o|a)?|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\b)\s+baño(s)?')
    anio_de_construccion = extraer_anio_construccion(texto,r'\b(19|20)\d{2}\b')
    return int(ascensor),num_habitaciones,num_baños,anio_de_construccion


#distritos = pd.read_csv('')

def get_coords(lugar):
    """Recibe un lugar en formato string y haciendo usa de la librería Nominatim obtenemos las
    coordenadas (latitud, longitud) de dicho lugar."""
    geolocator = Nominatim(user_agent="Usuario")
    address = f'{lugar}'
    location = geolocator.geocode(address)
    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
    else:
        latitude = longitude = np.NaN
    sleep(2)
    return pd.Series({"Latitud": latitude, "Longitude": longitude})


def transformar_localizacion(datos,urls):
    """Primero con las funciones leer_municipios() y leer_distritos_barrios() lee los distritos,
    barrios y municipios de Madrid, los inserta todos en un array y aplica la funcion get_distrito()
    a la columna localización. Creando así una nueva columna con el distrito o ciudad correcta."""
    nom_municipios = leer_municipios(urls[1])
    nom_distritos, nom_barrios = leer_distritos_barrios(urls[0])
    nom_localizaciones = np.append(nom_distritos,nom_barrios)
    nom_localizaciones = np.append(nom_localizaciones,nom_municipios)
    nom_localizaciones = arreglar_localizaciones(nom_localizaciones)
    datos["distrito/ciudad"] = datos["Localización"].apply(lambda x: get_distrito(x, nom_localizaciones))
    return datos



#Funciones auxiliares privadas

#Funciones auxiliares privadas
def buscar_palabra(texto, palabra):
    """Recibe un texto y una palabra y devuelve True si dicha palabra se encuentra en el texto"""
    # Convertir el texto y la palabra a minúsculas para hacer la búsqueda insensible a mayúsculas
    if not pd.isnull(texto):
        texto = texto.lower()
        palabra = palabra.lower()

    # Buscar la palabra en el texto utilizando una expresión regular
        resultado = re.search(r'\b' + re.escape(palabra) + r'(?=\s|\W|$)', texto)


        if resultado:
            return True
        else:
            return False
    return False

def extraer_numero_dormitorios_baños(texto,exp_regular):
    """Recibe un texto y una expresion regular y se encarga de devolver el numero de habitaciones en
    caso de encontrarlo en el texto, y en caso contrario devuleve None."""
    # Buscar un número seguido de la expresión "dormitorio(s)" o "habitación(es)"
    if not pd.isnull(texto):
        resultado = re.search(exp_regular, texto, re.IGNORECASE)

        if resultado:
            numero = resultado.group(1)
            # Convertir el número encontrado (que puede estar en dígitos o palabras) a su equivalente en dígitos
            if numero.isdigit():
                return int(numero)
            else:
                numeros_texto = {"un": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10}
                return numeros_texto.get(numero.lower(), None)
        else:
            return None  # Devuelve None si no se encontró ningún número de dormitorios o habitaciones
    return None

def extraer_anio_construccion(texto,exp_regular):
    """Recibe un texto y una expresion regular y se encarga de devolver el año de construcción en
    caso de encontrarlo en el texto, y en caso contrario devuleve None."""
    if not pd.isnull(texto):
        resultado = re.search(exp_regular, texto, re.IGNORECASE)
        if resultado:
            return resultado.group(0)
        else:
            return None

def leer_distritos_barrios(url):
    """Recibe una url y se encarga de leer el csv de la url. Devuelve dos arrays:
    uno con los nombres de los distritos y otro con los nombres de los barrios de Madrid"""
    datos_distritos = pd.read_csv(url,encoding='latin1',sep =";")
    nom_distritos = datos_distritos["distrito_nombre"].unique()
    nom_distritos = [s.strip() for s in nom_distritos]
    nom_barrios = datos_distritos["barrio_nombre"].unique()
    nom_barrios = [s.strip() for s in nom_barrios]
    return nom_distritos, nom_barrios

def leer_municipios(url):
    """Recibe una url y se encarga de leer el csv de la url. Devuelve un array con todos los
    municipios de madrid"""
    datos_municipios = pd.read_csv(url,encoding='latin1',sep =";")
    nom_municipios = datos_municipios["municipio_nombre"].unique()
    nom_municipios = [s.strip() for s in nom_municipios]
    return nom_municipios

def arreglar_localizaciones(nom_localizaciones):
    """Se encarga de arreglar el array de localizaciones para que no haya errores al aplicar
    la función get_distrito()"""
    nom_localizaciones = np.delete(nom_localizaciones, np.where(nom_localizaciones == "Centro"))
    nom_localizaciones = np.delete(nom_localizaciones, np.where(nom_localizaciones == "Madrid"))
    nom_localizaciones = np.append(nom_localizaciones,"El Molar")
    nom_localizaciones = np.append(nom_localizaciones,"El Álamo")
    nom_localizaciones = np.append(nom_localizaciones,"Rio")
    nom_localizaciones = np.append(nom_localizaciones,"Montecarmelo")
    nom_localizaciones = np.append(nom_localizaciones,"Arroyo Del Fresno")
    nom_localizaciones = np.append(nom_localizaciones,"Salvador")
    nom_localizaciones = np.append(nom_localizaciones,"Virgen del Cortijo")
    nom_localizaciones = np.append(nom_localizaciones,"San Cristóbal")
    nom_localizaciones = np.append(nom_localizaciones,"Moscardo")
    nom_localizaciones = np.append(nom_localizaciones,"Pilar")
    nom_localizaciones = np.append(nom_localizaciones,"Fuencarral")
    nom_localizaciones = np.append(nom_localizaciones,"Puerta Del Ángel")
    nom_localizaciones = np.append(nom_localizaciones,"Peñagrande")
    nom_localizaciones = np.append(nom_localizaciones,"Las Rozas De Madrid")
    nom_localizaciones = np.append(nom_localizaciones,"Los Santos De La Humosa")
    nom_localizaciones = np.append(nom_localizaciones,"Centro")
    nom_localizaciones = np.append(nom_localizaciones,"Madrid")
    return nom_localizaciones

def get_distrito(localizacion, nom_localizaciones):
    """Recibe una localización y una lista de localizaciones. Busca en la lista de localizaciones
     la localización dicha y si la encuentra la devuelve en caso contrario devuelve None."""
    for distrito in nom_localizaciones:
        if buscar_palabra(localizacion, distrito):
            return distrito
    return None

def imputar_valores(variables_entrada,variable_imputada,datos_viviendas):
    """Para evitar los NaNs predice o imputa utilizando regresión los valores para sustituir dichos NaNs."""
    df_known = datos_viviendas.dropna(subset=[variable_imputada])
    df_unknown = datos_viviendas[datos_viviendas[variable_imputada].isna()]

    # Entrenar el modelo de regresión lineal usando las variables de entrada e imputar la variable que queremos
    X_train = df_known[variables_entrada]
    y_train = df_known[variable_imputada]
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predecir los valores de año de construcción para los datos con valores faltantes
    X_pred = df_unknown[variables_entrada]
    predicted = model.predict(X_pred)

    # Asignar los valores predichos al DataFrame original
    datos_viviendas.loc[datos_viviendas[variable_imputada].isna(), variable_imputada] = predicted
