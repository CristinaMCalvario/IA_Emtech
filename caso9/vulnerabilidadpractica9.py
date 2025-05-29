import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def cargar_datos(nombre_archivo):
    """
    Carga los datos desde un archivo CSV y convierte variables categóricas en numéricas.
    Prueba con encoding utf-8 y si falla usa latin1.

    Parámetros:
    nombre_archivo (str): Ruta del archivo CSV.

    Retorna:
    pd.DataFrame: Datos preparados para el análisis.
    """
    try:
        datos = pd.read_csv(nombre_archivo, encoding='utf-8')
    except UnicodeDecodeError:
        print("Error con encoding utf-8, intentando con 'latin1'")
        datos = pd.read_csv(nombre_archivo, encoding='latin1')

    # Convertir variables categóricas a variables dummy (0/1)
    datos = pd.get_dummies(datos)

    # Revisar si la columna 'fraude' existe, y hacer limpieza básica
    if 'fraude' in datos.columns:
        if datos['fraude'].dtype == 'object':
            datos['fraude'] = datos['fraude'].map({'no': 0, 'sí': 1, 'si': 1}).fillna(0).astype(int)

        datos = datos.dropna(subset=['fraude'])
    else:
        raise ValueError("La columna 'fraude' no existe en el archivo de datos.")

    return datos

def entrenar_modelo(datos):
    """
    Entrena un modelo de regresión logística usando los datos cargados.

    Parámetros:
    datos (pd.DataFrame): Datos con variables independientes y la variable objetivo 'fraude'.

    Retorna:
    model (LogisticRegression): Modelo entrenado.
    """
    # Separar variables independientes (X) y variable objetivo (y), axis=1 para columnas
    # y axis=0 para filas
    # Asegurarse de que 'fraude' esté en la última columna  
    # .drop() en pandas se usa para eliminar columnas     
    X = datos.drop('fraude', axis=1)
    y = datos['fraude']

    # Verificar que y sea una serie 1D y contenga solo valores binarios
    print("Valores únicos en y:", y.unique())
    print("Tipo de datos de y:", y.dtype)
    print("Valores nulos en y:", y.isnull().sum())

    # Normalizar variables independientes para mejor rendimiento del modelo
   # Crea un objeto de la clase StandardScaler de Scikit-learn, diseñado para escalar (transformar) los datos numéricos.
    scaler = StandardScaler()
    #.fit_transform(X), Calcula la media ,desviación y moda estánda de cada columna de X y luego aplica la transformación para normalizar los datos.
    X_normalizado = scaler.fit_transform(X)

    # Crear modelo de regresión logística
    modelo = LogisticRegression()

    # Entrenar modelo con X normalizado y variable objetivo y
    modelo.fit(X_normalizado, y)

    return modelo, scaler

def predecir_riesgo(modelo, scaler, datos):
    """
    Usa el modelo entrenado para predecir riesgos en base a los datos.

    Parámetros:
    modelo (LogisticRegression): Modelo entrenado.
    scaler (StandardScaler): Objeto para normalizar datos.
    datos (pd.DataFrame): Datos con variables independientes (sin 'fraude').

    Retorna:
    list: Lista con etiquetas de riesgo (Muy alto, Alto, Medio, Bajo, Muy bajo).
    """
    # Eliminar variable objetivo si está en los datos (solo usar variables independientes)
    if 'fraude' in datos.columns:
        datos_sin_objetivo = datos.drop('fraude', axis=1)
    else:
        datos_sin_objetivo = datos.copy()

    # Normalizar datos con el scaler ya ajustado
    datos_normalizados = scaler.transform(datos_sin_objetivo)

    # Predecir probabilidades de clase negativa (sin fraude)
    probabilidades = modelo.predict_proba(datos_normalizados)

    # Convertir probabilidades a etiquetas de riesgo
    etiquetas_riesgo = []
    for prob in probabilidades:
        prob_sin_fraude = prob[0]  # Probabilidad de no fraude (clase 0)

        if prob_sin_fraude > 0.9:
            riesgo = "Muy bajo"
        elif prob_sin_fraude > 0.7:
            riesgo = "Bajo"
        elif prob_sin_fraude > 0.5:
            riesgo = "Medio"
        elif prob_sin_fraude > 0.3:
            riesgo = "Alto"
        else:
            riesgo = "Muy alto"

        etiquetas_riesgo.append(riesgo)

    return etiquetas_riesgo

if __name__ == "__main__":
    # Cargar los datos del archivo CSV
    datos = cargar_datos("compras.csv")

    # Entrenar el modelo y obtener el scaler
    modelo_entrenado, scaler_entrenado = entrenar_modelo(datos)

    # Predecir los riesgos en los mismos datos (o en datos nuevos si tienes)
    riesgos = predecir_riesgo(modelo_entrenado, scaler_entrenado, datos)

    # Mostrar las etiquetas de riesgo para cada registro. 
    #riesgos es una lista que contiene los valores de riesgo (por ejemplo, "Muy bajo", "Alto", etc.
    # enumerate(riesgos) es una función de Python que recorre la lista riesgos
    for i, riesgo in enumerate(riesgos):
        print(f"Registro {i + 1}: Riesgo = {riesgo}")