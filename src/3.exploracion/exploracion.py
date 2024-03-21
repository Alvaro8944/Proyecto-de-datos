import matplotlib.pyplot as plt
import seaborn as sns
import folium

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
            plt.title(f"{c}")

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

def histogramas(df):
    sns.set(style="whitegrid")

    fig, axs = plt.subplots(3, 2, figsize=(12, 10))

    sns.histplot(df["Precio"], kde=True, ax=axs[0, 0])
    axs[0, 0].set_title('Histograma de Precio')

    sns.histplot(df["Dormitorios"], kde=True, ax=axs[0, 1])
    axs[0, 1].set_title('Histograma de Dormitorios')

    sns.histplot(df["Superficie"], kde=True, ax=axs[1, 0])
    axs[1, 0].set_title('Histograma de Superficie')

    sns.histplot(df["Num_baños"], kde=True, ax=axs[1, 1])
    axs[1, 1].set_title('Histograma de Num_baños')

    sns.histplot(df["Año_de_construccion"], kde=True, ax=axs[2, 0])
    axs[2, 0].set_title('Histograma de Año_de_construccion')

    fig.delaxes(axs[2, 1])

    plt.tight_layout()
    plt.show()


def graf_puntos(df):
    sns.set(style="whitegrid")

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    sns.scatterplot(data=df, x="Superficie", y="Precio", ax=axs[0, 0], color="crimson")
    axs[0, 0].set_title('Precio vs. Superficie')

    sns.scatterplot(data=df, x="Dormitorios", y="Precio", ax=axs[0, 1], color="forestgreen")
    axs[0, 1].set_title('Precio vs. Dormitorios')

    sns.scatterplot(data=df, x="Num_baños", y="Precio", ax=axs[1, 0], color="gold")
    axs[1, 0].set_title('Precio vs. Num_baños')

    fig.delaxes(axs[1, 1])

    plt.tight_layout()
    plt.show()

def barras_tipo_etiqueta(df):
    # Contar el número de instancias para cada valor de la característica categórica
    count_data = df.groupby('Tipo_de_inmueble')['Etiqueta'].value_counts().unstack(fill_value=0)

    # Configurar el estilo de los gráficos
    sns.set(style="whitegrid")

    # Crear el gráfico de barras
    ax = count_data.plot(kind='bar', stacked=True, figsize=(10, 6))

    # Añadir etiquetas y título
    ax.set_ylabel('Número de Propiedades')
    ax.set_xlabel('Tipo de Inmueble')
    ax.set_title('Distribución de Propiedades por Tipo e Etiqueta')

    # Mostrar el gráfico
    plt.xticks(rotation=0)
    plt.legend(title='Etiqueta')
    plt.tight_layout()
    plt.show()