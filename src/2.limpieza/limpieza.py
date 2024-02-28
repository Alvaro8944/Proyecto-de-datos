import numpy as np
import pandas as pd
import re
from time import sleep
from geopy.geocoders import Nominatim


# Lee el archivo CSV y almacena su contenido en un DataFrame
datos = pd.read_csv('C:/Users/dalon/Desktop/UCM/2º/PROYECTO_DATOS_I/Casas_todas.csv',usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
print(datos.head())

#Funciones publicas

def string_to_int(x):
    if not pd.isnull(x):
        x_split = x.split()
        return int(x_split[0])
    else:
        return np.nan

def obtener_tipo_casa(x):
    return x.split("/")[4]

def string_to_price(x):
    return pd.to_numeric(x.split()[0].replace(".",""),errors='coerce')

def string_to_dicotomic(x):
    if not pd.isnull(x):
        return 1
    else:
        return 0

def transformar_en_dicotomicas(datos):
    columnasDicotomicas = ["Calefaccion","Ascensor","Aire acondicionado","Jardin"]
    for columna in columnasDicotomicas:
        datos[columna] = datos[columna].replace("No disponible",np.nan)
        datos[columna] = datos[columna].apply(string_to_dicotomic)
    return datos

def analizar_descripcion(texto):
    ascensor = buscar_palabra(texto, "ascensor")
    reformar = buscar_palabra(texto, "reformar")
    num_habitaciones = extraer_numero_dormitorios(texto)
    num_baños = extraer_numero_dormitorios(texto)
    return int(ascensor),int(reformar),num_habitaciones,num_baños


distritos = pd.read_csv('')

def get_coords(lugar):
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


df = pd.DataFrame({"Neighbourhood": ("Alcorcón",
                                     "Mostoles",
                                     "Las Rozas de Madrid",
                                     "Madrid centro"
                                     )})

lldata = pd.concat([df, df.Neighbourhood.apply(get_coords)], axis=1)




#Funciones auxiliares privadas

def buscar_palabra(texto, palabra):
    # Convertir el texto y la palabra a minúsculas para hacer la búsqueda insensible a mayúsculas
    texto = texto.lower()
    palabra = palabra.lower()

    # Buscar la palabra en el texto utilizando una expresión regular
    resultado = re.search(r'\b' + re.escape(palabra) + r'(?=\s|\W|$)', texto)


    if resultado:
        return True
    else:
        return False

def extraer_numero_dormitorios(texto):
    # Buscar un número seguido de la expresión "dormitorio(s)" o "habitación(es) o baño(s)"
    resultado = re.search(r'(\b\d+\b|(un(o|a)?|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\b)\s+(dormitorio|habitación|baño)(es|s)?', texto, re.IGNORECASE)

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


def leer_distritos_barrios():
    datos_distritos = pd.read_csv('C:/Users/dalon/Desktop/UCM/2º/PROYECTO_DATOS_I/barrios_municipio_madrid.csv',encoding='latin1',sep =";")
    nom_distritos = datos_distritos["distrito_nombre"].unique()
    nom_distritos = [s.strip() for s in nom_distritos]
    nom_barrios = datos_distritos["barrio_nombre"].unique()
    nom_barrios = [s.strip() for s in nom_barrios]
    return nom_distritos, nom_barrios

def leer_municipios():
    datos_municipios = pd.read_csv('C:/Users/dalon/Desktop/UCM/2º/PROYECTO_DATOS_I/municipio_comunidad_madrid.csv',encoding='latin1',sep =";")
    nom_municipios = datos_municipios["municipio_nombre"].unique()
    nom_municipios = [s.strip() for s in nom_municipios]
    return nom_municipios

def arreglar_localizaciones(nom_localizaciones):
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
    for distrito in nom_localizaciones:
        if buscar_palabra(localizacion, distrito):
            return distrito
    return None

def transformar_localizacion(datos):
    nom_distritos, nom_barrios = leer_distritos_barrios()
    nom_municipios = leer_municipios()
    nom_localizaciones = np.append(nom_distritos,nom_barrios)
    nom_localizaciones = np.append(nom_localizaciones,nom_municipios)
    nom_localizaciones = arreglar_localizaciones(nom_localizaciones)
    datos["distrito/ciudad"] = datos["Localización"].apply(lambda x: get_distrito(x, nom_localizaciones))
    return datos