from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def load_logs(filename):
    """
    Carga los registros de seguridad desde un archivo de texto.
    
    Args:
        filename (str): Ruta del archivo de registros.
    
    Returns:
        list[str]: Lista de líneas (registros) sin saltos de línea.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            logs = file.readlines()
        return [log.strip() for log in logs]
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encontró.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def extract_features(logs):
    """
    Convierte los registros de texto en vectores numéricos usando TF-IDF.

    Args:
        logs (list[str]): Lista de registros de texto.

    Returns:
        scipy.sparse matrix: Matriz de características numéricas.
    """
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(logs)

def train_model(features, labels):
    """
    Entrena un modelo de regresión logística con los datos proporcionados.

    Args:
        features: Matriz de características.
        labels (list[int]): Etiquetas binarias (1 para intrusión, 0 para normal).
    
    Returns:
        LogisticRegression: Modelo entrenado.
    """
    model = LogisticRegression()
    model.fit(features, labels)
    return model

def predict_labels(model, features):
    """
    Usa el modelo entrenado para predecir etiquetas de nuevos datos.

    Args:
        model: Modelo entrenado.
        features: Matriz de características.
    
    Returns:
        list[int]: Predicciones (1 o 0).
    """
    return model.predict(features)

if __name__ == "__main__":
    # Ruta del archivo con los registros
    archivo_logs = "logs.txt"

    # Cargar los registros
    logs = load_logs(archivo_logs)
    
    if logs:
        # Crear etiquetas: 1 si empieza con "Intrusion", 0 en otro caso
        labels = [1 if log.startswith("Intrusion") else 0 for log in logs]

        # Extraer características numéricas
        features = extract_features(logs)

        # Entrenar el modelo con las características y etiquetas
        model = train_model(features, labels)

        # Predecir etiquetas para los mismos registros (solo como ejemplo)
        predictions = predict_labels(model, features)

        # Mostrar predicciones
        for i, prediction in enumerate(predictions):
            print(f"Registro: {logs[i]} → Predicción: {'Intrusión' if prediction == 1 else 'Normal'}")