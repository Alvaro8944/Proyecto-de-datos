import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFE
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
import mlflow
import mlflow.sklearn



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

 def calcular_error(model,X,y):
    test_predictions = model.predict(X)
    test_mse = mean_absolute_error(y, test_predictions)
    return test_mse

class CustomRFE(RFE):
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


def guardar_resultados_mlflow(diccionario_resultados, nombre_modelo, model):
    mlflow.set_experiment("ProyectoDeDatos")  # Nombre de tu experimento en MLflow
    with mlflow.start_run() as run:
        for key in diccionario_resultados.keys():
            try:
                if key == 'best_params':
                    for param_key, param_value in diccionario_resultados[key].items():
                        mlflow.log_param(f'best_{param_key}', param_value)
                elif key == 'cross_validation':
                    for dic in diccionario_resultados[key]:
                        log_metric_text = ""
                        for key,value in dic.items():
                            if key != "test_score":
                                log_metric_text+= f" {key}_ {value}"
                            else:
                                metric = value
                        mlflow.log_metric(log_metric_text,metric)
                elif "error" in key:
                    mlflow.log_metric(key, diccionario_resultados[key])
                else:
                    mlflow.log_param(key, diccionario_resultados[key])
            except KeyError as e:
                print(f"Error al procesar la clave {key}: {str(e)}")
                # Puedes agregar aquí otro manejo de errores o simplemente continuar
        mlflow.sklearn.log_model(model, nombre_modelo)

def linear_regresion_model(X,y):
    resultados = {}
    model = LinearRegression()
    model.fit(X,y)
    validation_error = calcular_error(model,X,y)
    resultados = crear_resguardo_modelo(nombre_modelo="linear_regression",validation_error=validation_error,cross_validation=False,stratify=True,RFE=False,grid =False)

    return model,resultados

def linear_regression_cross_validation(X,y):
    linear_reg = LinearRegression()

    param_grid = {
    'fit_intercept': [True, False],
    'normalize': [True, False],
    'positive': [True, False]
    }

    grid_search = GridSearchCV(estimator=linear_reg, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')

    grid_search.fit(X, y)

    param_grid_dictionary =  {key: "" for key in param_grid.keys()}

    resultados = crear_resguardo_modelo(nombre_modelo="linear_regression_model_cv",validation_error=grid_search.best_score_,cross_validation=True,stratify=True,RFE=False,grid=True,best_params=grid_search.best_params_,param_grid_dictionary=param_grid_dictionary,results=grid_search.cv_results_)


    return grid_search.best_estimator_, resultados


def get_related_features(X):
    related_group = []
    related_groups_name = ["Tipo_de_inmueble", "Etiqueta","Tipo_"]
    for name in related_groups_name:
        columnas_filtradas = X.filter(regex=name)
        selected_column_names = columnas_filtradas.columns
        related_features_index = [X.columns.get_loc(col_name) for col_name in selected_column_names]
        related_group.append(related_features_index)
    return related_group


def get_protected_features(X):
    columnas_filtradas = X.filter(regex='distrito|ciudad_')
    selected_column_names = columnas_filtradas.columns
    protected_features_index = [X.columns.get_loc(col_name) for col_name in selected_column_names]
    return protected_features_index


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV

def linear_regression_model_rfe(X, y,custom):


    related_group = None
    protected_features_index = None

    if custom:
        related_group = get_related_features(X);
        protected_features_index = get_protected_features(X)


    rfe = CustomRFE(estimator=LinearRegression(), groups=related_group, protected_features=protected_features_index)

    # Aplica el CustomRFE a tus datos
    rfe.fit(X, y)

    # Obtén las características seleccionadas
    selected_features = rfe.support_
    columnas_seleccionadas = X.columns[selected_features]
    X_RFE = X[columnas_seleccionadas]

    linear_reg = LinearRegression()

    param_grid = {
    'fit_intercept': [True, False],
    'normalize': [True, False],
    'positive': [True, False]
    }

    grid_search = GridSearchCV(estimator=linear_reg, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')

    grid_search.fit(X_RFE, y)

    resultados = crear_resguardo_modelo(nombre_modelo="linear_regression_model_grid_cv_rfe",validation_error=grid_search.best_score_,cross_validation=True,stratify=True,RFE=True,grid=True,best_params=grid_search.best_params_,param_grid_dictionary=param_grid_dictionary,results=grid_search.cv_results_)

    return grid_search.best_estimator_, resultados, columnas_seleccionadas

