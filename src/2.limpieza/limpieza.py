import numpy as np
import pandas as pd
import re


# Lee el archivo CSV y almacena su contenido en un DataFrame
datos = pd.read_csv('C:/Users/dalon/Desktop/UCM/2º/PROYECTO_DATOS_I/Casas_todas.csv',usecols = lambda columna: columna!= "Unnamed: 0")

# Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
print(datos.head())

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
    # Buscar un número seguido de la expresión "dormitorio(s)" o "habitación(es)"
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
