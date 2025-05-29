from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import sqlite3
import pandas as pd  # Para tabular la salida en consola
import re  # Para validación de caracteres

# ===== IMPORTS DE MACHINE LEARNING PARA DETECCIÓN DE CONTENIDO SOSPECHOSO =====
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Datos de entrenamiento para el modelo (simulados para este ejercicio)
ejemplos_logs = [
    "Intrusion from unknown IP",
    "Product added to cart",
    "System alert Intrusion",
    "New user registration",
    "Intrusion detected",
    "User purchased item"
]
etiquetas = [1, 0, 1, 0, 1, 0]  # 1: sospechoso, 0: normal

# ===== INICIO: MODELO DE MACHINE LEARNING =====

# Creamos un vectorizador que convierte texto en vectores numéricos usando TF-IDF
vectorizer = TfidfVectorizer()

# Transformamos los ejemplos de logs en vectores numéricos
X = vectorizer.fit_transform(ejemplos_logs)

# Creamos el modelo de regresión logística para clasificación binaria
modelo_ml = LogisticRegression()

# Entrenamos el modelo con los datos de entrada (X) y las etiquetas (etiquetas)
modelo_ml.fit(X, etiquetas)

# ===== FIN: MODELO DE MACHINE LEARNING =====

# ===== FUNCIONES DE BASE DE DATOS =====
def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            precio TEXT
        )
    ''')
    conn.commit()
    conn.close()

def obtener_productos():
    """Recupera los productos desde la base de datos y los devuelve como lista."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, descripcion, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# ===== INTERFAZ GRÁFICA KIVY =====
class ProductPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text='Nombre del Producto:'))
        self.product_name = TextInput(multiline=False)
        self.add_widget(self.product_name)

        self.add_widget(Label(text='Descripción:'))
        self.product_description = TextInput(multiline=False)
        self.add_widget(self.product_description)

        self.add_widget(Label(text='Precio:'))
        self.product_price = TextInput(multiline=False)
        self.add_widget(self.product_price)

        self.add_product_button = Button(text='Guardar Producto')
        self.add_product_button.bind(on_press=self.save_product)
        self.add_widget(self.add_product_button)

        self.view_products_button = Button(text='Ver Productos en Consola')
        self.view_products_button.bind(on_press=self.show_products)
        self.add_widget(self.view_products_button)

        self.product_list_label = Label(text='Estado: Esperando acción...')
        self.add_widget(self.product_list_label)

    def save_product(self, instance):
        """Guarda un producto en la base de datos y aplica modelo ML para detección."""
        name = self.product_name.text.strip()
        description = self.product_description.text.strip()
        price = self.product_price.text.strip()

        # ===== VALIDACIONES =====
        if not name or not re.match(r'^[\w\s.,;:!?()-]+$', name):
            self.product_list_label.text = '❌ Nombre inválido: vacío o contiene caracteres no permitidos.'
            return

        try:
            precio_num = float(price)
            if precio_num <= 0:
                raise ValueError
        except ValueError:
            self.product_list_label.text = '❌ Precio inválido: debe ser numérico y mayor que 0.'
            return

        if not description:
            self.product_list_label.text = '❌ La descripción no puede estar vacía.'
            return

        # ===== Análisis de contenido con modelo ML =====
        texto_a_analizar = [name + " " + description]
        vector = vectorizer.transform(texto_a_analizar)
        prediccion = modelo_ml.predict(vector)[0]

        if prediccion == 1:
            self.product_list_label.text = '⚠️ Contenido sospechoso detectado. No se guardó.'
            return

        # ===== Guardar en la base de datos =====
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)",
                       (name, description, price))
        conn.commit()
        conn.close()

        self.product_name.text = ''
        self.product_description.text = ''
        self.product_price.text = ''
        self.product_list_label.text = '✅ Producto guardado correctamente.'

    def show_products(self, instance):
        """Muestra los productos guardados en consola usando pandas."""
        productos = obtener_productos()
        if productos:
            df = pd.DataFrame(productos, columns=["Nombre", "Descripción", "Precio"])
            print("\n📦 Productos registrados:\n")
            print(df.to_string(index=False))
            self.product_list_label.text = f'Se mostraron {len(df)} productos en la consola.'
        else:
            self.product_list_label.text = 'No hay productos guardados aún.'

class ProductApp(App):
    def build(self):
        return ProductPanel()

if __name__ == '__main__':
    init_db()
    ProductApp().run()