import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFE
from sklearn.base import clone
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, RandomizedSearchCV
from scipy.stats import uniform
from IPython.display import display
from sklearn.feature_selection import RFECV
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import numpy as np

import mlflow
import mlflow.sklearn

def create_model_backup(nombre_modelo,validation_error,cross_validation,stratify,RFE,grid,best_params = None,param_grid_dictionary= None,results=None,solver =None):
    """ recibe una serie de parametros y crea una diccionario con todos ello que posteriormente será usado
    para guardar toda la información del modelo en mlflow"""
    resultados = {}
    print(nombre_modelo)
    resultados["Modelo"] = nombre_modelo
    resultados["stratify"] = stratify
    resultados["rfe"] = RFE
    resultados["cv"] = cross_validation
    if solver:
        resultados["solver"] =solver
    if best_params is not None:
        resultados["mean_validation_error"] = validation_error
        resultados["best_params"] = best_params
        resultados_cv = []
    # Iterar sobre los resultados y agregarlos a la lista de resultados de Ridge
        for mean_score, params in zip(results['mean_test_score'], results['params']):
            dictionary = param_grid_dictionary.copy()
            for key, value in params.items():
                if not isinstance(value,str) and value <0:
                    print(value)
                    value= -value
                param_grid_dictionary[key] = value
            dictionary["validation_error"] = -mean_score
            resultados_cv.append(dictionary)
    # Agregar la lista de resultados de Ridge al diccionario de resultados
        resultados["cross_validation"] = resultados_cv
    else:
        resultados["train_error"] = validation_error

    return resultados;

def save_results_mlflow(diccionario_resultados, nombre_modelo, model):
    """ recibe un diccionario de los resultados creado por create_model_backup(),el nombre del modelo
    y el modelo  y lo guarda en mlflow """
    ##mlflow.set_tracking_uri(None)
    mlflow.set_tracking_uri("sqlite:////Users/hamzatriki/BasesDeDatosMlfow2.db")
    mlflow.set_experiment("ProyectoTecnocasa")  # Nombre de tu experimento en MLflow
    with mlflow.start_run() as run:
        metric = 0.0
        for key in diccionario_resultados.keys():
            try:
                if key == 'best_params':
                    for param_key, param_value in diccionario_resultados[key].items():
                        mlflow.log_param(f'best_{param_key}', param_value)
                elif key == 'cross_validation':
                    for dic in diccionario_resultados[key]:
                        log_metric_text = ""
                        for key,value in dic.items():
                            if key != "train_score":
                                log_metric_text+= f" {key}_ {value}"
                            else:
                                metric = value
                        mlflow.log_metric(log_metric_text, metric)
                elif "error" in key:
                    mlflow.log_metric(key, diccionario_resultados[key])
                else:
                    mlflow.log_param(key, diccionario_resultados[key])
            except KeyError as e:
                print(f"Error al procesar la clave {key}: {str(e)}")
        mlflow.sklearn.log_model(model, nombre_modelo)

def split_train_trest(X,y,stratify =None):
    """recibe los datos y un parametro de stratificación y devuelve el train y test.
    se usa una semilla para obtener siempre los mismos datos."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify = stratify, random_state=42)
    return X_train, X_test, y_train, y_test

def one_hot_encoder(data):
    """recibe una lista de datos(X_train,X_test) y les realiza el one_hot_encodging"""
    encoded_data = []
    for dato in data:
        if isinstance(dato, pd.Series):
            dato = pd.DataFrame(dato)
        categorical_columns = dato.select_dtypes(include=["object"]).columns
        encoder = OneHotEncoder(sparse=False)
        encoded_columns = encoder.fit_transform(dato[categorical_columns])
        new_columns = encoder.get_feature_names_out(categorical_columns)
        data_encoded = pd.DataFrame(encoded_columns, columns=new_columns)
        dato.reset_index(drop=True, inplace=True)
        data_encoded.reset_index(drop=True, inplace=True)
        dato_encoded = pd.concat([dato.drop(categorical_columns, axis=1), data_encoded], axis=1)
        encoded_data.append(dato_encoded)

    return encoded_data[0], encoded_data[1]

def standardize(X_train,X_test):
    """recibe los datos y los estandariza"""
    scaler = StandardScaler()
    variables_estandarizar = ["Dormitorios","Superficie","Num_baños","Año_de_construccion","Latitud","Longitud"]
    X_train_encoded_scaled = X_train.copy()
    X_test_encoded_scaled = X_test.copy()
    X_train_encoded_scaled[variables_estandarizar] = scaler.fit_transform(X_train[variables_estandarizar])
    X_test_encoded_scaled[variables_estandarizar] = scaler.transform(X_test[variables_estandarizar])
    return X_train_encoded_scaled,X_test_encoded_scaled

def calculate_error(model,X,y):
    """ recibe un modelo y los datos y calcula el error del modelo"""
    test_predictions = model.predict(X)
    test_mse = mean_absolute_error(y, test_predictions)
    return test_mse

def linear_regresion_model(X,y):
    """ recibe los datos y devuelve el modelo y un diccionario con los resultados"""
    resultados = {}
    model = LinearRegression()
    model.fit(X,y)
    validation_error = calculate_error(model,X,y)
    resultados = create_model_backup(nombre_modelo="linear_regression",validation_error=validation_error,cross_validation=False,stratify=True,RFE=False,grid =False)
    return model,resultados



def regularization_model_cross_validation(X_train_encoded, y_train,param_grid,model,random):
    """ recibe los datos,el param_grid,el modelo y random (un boleano para saber si
    usar grid_search o ramdom_search).Esta función sirve para todos los modelos
    deregularización(Ridge,Lasso,ElasticNet). Devuelve un diccionario y el mejor modelo."""

    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    if random:
        grid_search = RandomizedSearchCV(model, param_distributions=param_grid, n_iter=100,scoring='neg_mean_absolute_error', cv=kfold, random_state=42)
    else:
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=kfold, scoring='neg_mean_absolute_error')


    grid_search.fit(X_train_encoded, y_train)
    param_grid_dictionary =  {key: "" for key in param_grid.keys()}

    resultados = create_model_backup(nombre_modelo=f"{type(model).__name__}_regression_model_grid_cv_rfe",validation_error=-grid_search.best_score_,cross_validation=True,stratify=True,RFE=False,grid=True,best_params=grid_search.best_params_,param_grid_dictionary=param_grid_dictionary,results=grid_search.cv_results_)

    return grid_search.best_estimator_,resultados


def get_related_features(X):
    """Recibe los datos y devuelve los columnas que son relacionadas, son columnas que antes eran una pero al
    aplicar el one-hot-enconing ya no"""
    related_group = []
    related_groups_name = ["Tipo_de_inmueble", "Etiqueta","Tipo_"]
    for name in related_groups_name:
        columnas_filtradas = X.filter(regex=name)
        selected_column_names = columnas_filtradas.columns
        related_features_index = [X.columns.get_loc(col_name) for col_name in selected_column_names]
        related_group.append(related_features_index)
    return related_group
def get_protected_features(X):
    """devuelve las columnas protegidas,que son la de los distritos"""
    columnas_filtradas = X.filter(regex='distrito|ciudad_')
    selected_column_names = columnas_filtradas.columns
    protected_features_index = [X.columns.get_loc(col_name) for col_name in selected_column_names]
    return protected_features_index

class CustomRFE(RFE):
    """Modificación de la clase RFE para que no elimine nunca las variables de localización.Si elimina
    una variable del grupo de related_features, elimnara el resto"""
    def __init__(self, estimator, n_features_to_select=None, step=1, groups=None, protected_features=None):
        super().__init__(estimator, n_features_to_select=n_features_to_select, step=step)
        self.groups = groups
        self.protected_features = protected_features

    def fit(self, X, y):
        self.support_ = np.ones(X.shape[1], dtype=bool)
        estimator = clone(self.estimator)
        super().fit(X, y)
        if self.groups or self.protected_features:
            for idx, selected in enumerate(self.support_):
                if not selected:
                    for related_features in self.groups:
                        if idx in related_features:
                            for feature_idx in related_features:
                                self.support_[feature_idx] = False
                    if idx in self.protected_features:
                        self.support_[idx] = True
        return self


def polinomical_regression_model_rfe(X, y,custom):
    """recibe los datos y un parametro custom, dependiendo de su valor, realiza el rfe customizado o no.
    Entrenama un modelo polinomico con grid_search y devuelve las columnas seleccionadas, el diccionario de
    resultados y las columnas seleccionadas.
    """

    related_group = None
    protected_features_index = None

    if custom:
        related_group = get_related_features(X);
        protected_features_index = get_protected_features(X)


    rfe = CustomRFE(estimator=Ridge(random_state =42), groups=related_group, protected_features=protected_features_index)

    # Aplica el CustomRFE a tus datos
    rfe.fit(X, y)

    # Obtén las características seleccionadas
    selected_features = rfe.support_
    columnas_seleccionadas = X.columns[selected_features]
    X_RFE = X[columnas_seleccionadas]



    param_grid = {
    'alpha': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,14,15,16,17,18,20,22,24,26,28,30,35,40,45,50],
    'tol': [1e-2,1e-3, 1e-4,]
    }

    param_grid_dictionary =  {key: "" for key in param_grid.keys()}

    kfold = KFold(n_splits=5, shuffle=True, random_state=42)

    grid_search = GridSearchCV(estimator=Ridge(random_state =42), param_grid=param_grid, cv=kfold, scoring='neg_mean_absolute_error')

    grid_search.fit(X_RFE, y)

    resultados = create_model_backup(nombre_modelo="linear_regression_model_grid_cv_rfe",validation_error=-grid_search.best_score_,cross_validation=True,stratify=True,RFE=True,grid=True,best_params=grid_search.best_params_,param_grid_dictionary=param_grid_dictionary,results=grid_search.cv_results_)

    return grid_search.best_estimator_, resultados, columnas_seleccionadas
