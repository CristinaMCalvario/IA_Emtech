# Importamos las librerías necesarias
import requests  # Para hacer solicitudes HTTP a una URL
import time      # Para medir el tiempo y pausar el monitoreo

def get_response_time(url):
    """
    Realiza una solicitud HTTP GET a la URL proporcionada y calcula
    cuánto tiempo tardó en obtener la respuesta.
    """
    # requests.get(url) envía una solicitud GET, HTTP GET a la URL
    response = requests.get(url)

    # Obtenemos el tiempo de respuesta en segundos desde que se envió hasta que se recibió
    # .elapsed es un objeto timedelta, y .total_seconds() lo convierte a segundos flotantes
    response_time = response.elapsed.total_seconds()

    # Retornamos el tiempo de respuesta
    return response_time

def monitor_performance(url, threshold):
    """
    Verifica el rendimiento de una URL comparando el tiempo de respuesta
    con un umbral definido por el usuario.
    """
    # Llama a la función que obtiene el tiempo de respuesta actual
    response_time = get_response_time(url)

    # Compara el tiempo de respuesta con el umbral definido
    if response_time > threshold:
        # Si se excede el umbral, se imprime una alerta con la información relevante
        print(
            "ALERTA: El tiempo de respuesta de la URL '{}' es de {:.2f} segundos. "
            "Esto supera el umbral de {:.2f} segundos.".format(url, response_time, threshold)
        )
    else:
        # Si está dentro del rango normal, se muestra un mensaje informativo
        print(
            "OK: El tiempo de respuesta de '{}' es {:.2f} segundos, dentro del umbral.".format(url, response_time)
        )

if __name__ == "__main__":
    """
    Bloque principal del programa: define la URL a monitorear y el umbral
    y ejecuta el monitoreo en un bucle continuo.
    """
    # Definimos la URL de la aplicación web a monitorear
    #url = "https://www.google.com"
    #url = "https://www.example.com"
    url = "http://127.0.0.1:5000/users"
    #url = "http://127.0.0.1:5000"
    #url = "http://localhost/phpmyadmin"
   
    # Definimos el umbral de tiempo de respuesta permitido (en segundos)
    threshold = 2.0

    # Inicia un bucle infinito que monitorea la URL cada segundo
    while True:
        # Llama a la función que evalúa el rendimiento
        monitor_performance(url, threshold)

        # Espera 1 segundo antes de volver a comprobar
        time.sleep(1.0)