import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFE
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder




def crear_resguardo_modelo(nombre_modelo,validation_error,cross_validation,stratify,RFE,grid,best_params = None,param_grid_dictionary= None,results=None):
    resultados = {}
    print(nombre_modelo)
    resultados["Modelo"] = nombre_modelo
    resultados["validation_error"] = validation_error
    resultados["stratify"] = stratify
    resultados["RFE"] = RFE
    resultados["CV"] = cross_validation
    if best_params is not None:
        resultados["best_params"] = best_params
        resultados_cv = []
        for mean_score, params in zip(results['mean_test_score'], results['params']):
            dictionary = param_grid_dictionary.copy()
            for key, value in params.items():
                param_grid_dictionary[key] = value
            dictionary["test_score"] = mean_score
            resultados_cv.append(dictionary)
        resultados["cross_validation"] = resultados_cv
    return resultados;

def split_train_trest(X,y,stratify =None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify = stratify, random_state=42)
    return X_train, X_test, y_train, y_test



def one_hot_encoder(data):
    encoded_data = []
    for dato in data:
        if isinstance(dato, pd.Series):
            dato = pd.DataFrame(dato)
        # Seleccionar las columnas categoricas
        categorical_columns = dato.select_dtypes(include=["object"]).columns
        encoder = OneHotEncoder(sparse=False)
        ## Aplicar One Hot Encoding
        encoded_columns = encoder.fit_transform(dato[categorical_columns])
        # Recuperar el nombre de las columnas
        new_columns = encoder.get_feature_names_out(categorical_columns)
        # Crear un DataFrame con los datos codificados y el nombre de las columnas
        data_encoded = pd.DataFrame(encoded_columns, columns=new_columns)
        # Resetear index
        dato.reset_index(drop=True, inplace=True)
        data_encoded.reset_index(drop=True, inplace=True)
        # Concatenar por columnas ambos DataFrames
        dato_encoded = pd.concat([dato.drop(categorical_columns, axis=1), data_encoded], axis=1)
        # Agregar el DataFrame codificado a la lista
        encoded_data.append(dato_encoded)

    return encoded_data[0], encoded_data[1]

