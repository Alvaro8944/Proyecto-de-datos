import pandas as pd

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


