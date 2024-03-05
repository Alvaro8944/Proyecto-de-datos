import matplotlib.pyplot as plt
import seaborn as sns

def correlacion(data):
    """Muestra de forma gráfica la correlación entre las variables"""
    correlation_matrix = data.corr()
    correlation_matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlación')
    plt.show()

def drop_cualitativas(datos):
    """Recibe el dataframe y devuelve otro con solo columnas numericas"""
    columna_a_eliminar = 'Descripción'
    df_drop = datos.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Etiqueta'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'distrito/ciudad'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Tipo_de_inmueble'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Tipo'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Metro'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Renfe'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Calefaccion'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Aire acondicionado'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Ascensor'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    columna_a_eliminar = 'Jardin'
    df_drop = df_drop.drop(columna_a_eliminar, axis=1)

    return df_drop

def boxplots(datos):
    """Recibe un dataframe y muestra por pantalla los boxplots de sus columnas las cuales tienen
    sentido ser estudiadas mediante un boxplot"""
    i = 0

    for c in datos.columns:
        if (i == 0):
            i = i + 1
        else:
            plt.boxplot(datos[c])

            # Añade un título al gráfico
            plt.title("Boxplot de una sola columna")

            # Añade etiquetas al eje x
            plt.xticks([1], [c])

            # Muestra el gráfico
            plt.show()

def revisar_coordenadas(datos):
    """Recibe el dataframe y crea otro dataframe con los valores que parecen
    outliers en las coordenadas (Latitud y Longitud). Solo necesitamos revisar la
    latitud ya que revisando la longitud no se encuentran mas valores erroneos"""
    filtro = (datos['Latitud'] > 41.5) | (datos['Latitud'] < 20)
    df_outliers_latitud = datos[filtro]
    df_outliers_latitud = df_outliers_latitud.reset_index(drop=True)

    print(df_outliers_latitud)