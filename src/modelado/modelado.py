import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFE
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split



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
