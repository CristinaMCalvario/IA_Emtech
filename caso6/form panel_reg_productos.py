from kivy.app import App  # Importa la clase principal de la aplicación Kivy
from kivy.uix.boxlayout import BoxLayout  # Importa el diseño de caja para organizar widgets
from kivy.uix.button import Button  # Importa la clase Button para agregar botones
from kivy.uix.label import Label  # Importa la clase Label para mostrar texto
from kivy.uix.textinput import TextInput  # Importa la clase TextInput para ingresar texto
import sqlite3  # Importa la librería SQLite para gestionar la base de datos

# Conectar a la base de datos SQLite y crear la tabla si no existe
def init_db():
    conn = sqlite3.connect('productos.db')  # Crea o abre la base de datos llamada 'productos.db'
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nombre TEXT,  
            descripcion TEXT,  
            precio TEXT 
        )
    ''')
    conn.commit()  # Guarda los cambios
    conn.close()  # Cierra la conexión con la base de datos

class ProductPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)  # Configura el diseño vertical
        
        # Etiqueta y campo de entrada para el nombre del producto
        self.add_widget(Label(text='Nombre del Producto:'))
        self.product_name = TextInput(multiline=False)  # Campo de texto de una sola línea
        self.add_widget(self.product_name)
        
        # Etiqueta y campo de entrada para la descripción del producto
        self.add_widget(Label(text='Descripción:'))
        self.product_description = TextInput(multiline=False)  # Campo de texto de una sola línea
        self.add_widget(self.product_description)
        
        # Etiqueta y campo de entrada para el precio del producto
        self.add_widget(Label(text='Precio:'))
        self.product_price = TextInput(multiline=False)  # Campo de texto de una sola línea
        self.add_widget(self.product_price)
        
        # Botón para guardar el producto en la base de datos
        self.add_product_button = Button(text='Guardar Producto')
        self.add_product_button.bind(on_press=self.save_product)  # Asigna la función al botón
        self.add_widget(self.add_product_button)
        
        # Botón para ver los productos guardados
        self.view_products_button = Button(text='Ver Productos Capturados')
        self.view_products_button.bind(on_press=self.show_products)  # Asigna la función al botón
        self.add_widget(self.view_products_button)
        
        # Etiqueta para mostrar los productos registrados
        self.product_list_label = Label(text='Productos registrados aparecerán aquí')
        self.add_widget(self.product_list_label)
    
    def save_product(self, instance):
        """Guarda un producto en la base de datos SQLite y limpia los campos de entrada."""
        name = self.product_name.text  # Obtiene el nombre del producto
        description = self.product_description.text  # Obtiene la descripción del producto
        price = self.product_price.text  # Obtiene el precio del producto
        
        if name and description and price:  # Verifica que todos los campos estén completos
            conn = sqlite3.connect('productos.db')  # Conecta a la base de datos
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)", (name, description, price))
            conn.commit()  # Guarda los cambios
            conn.close()  # Cierra la conexión
            
            # Limpia los campos de entrada
            self.product_name.text = ''
            self.product_description.text = ''
            self.product_price.text = ''
            
            self.product_list_label.text = 'Producto guardado correctamente!'  # Muestra mensaje de éxito
        else:
            self.product_list_label.text = 'Por favor, completa todos los campos.'  # Mensaje de error
    
    def show_products(self, instance):
        """Muestra la lista de productos guardados en la base de datos."""
        conn = sqlite3.connect('productos.db')  # Conecta a la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, descripcion, precio FROM productos")  # Obtiene todos los productos
        productos = cursor.fetchall()  # Recupera los datos
        conn.close()  # Cierra la conexión
        
        if productos:  # Si hay productos guardados, los muestra
            productos_texto = '\n'.join([f"{p[0]} - {p[1]} - ${p[2]}" for p in productos])  # Formatea la lista de productos
            self.product_list_label.text = productos_texto  # Muestra los productos en la etiqueta
        else:
            self.product_list_label.text = 'No hay productos guardados aún.'  # Mensaje si no hay productos

class ProductApp(App):
    def build(self):
        """Construye la aplicación con el panel de productos."""
        return ProductPanel()

if __name__ == '__main__':
    init_db()  # Inicializa la base de datos
    ProductApp().run()  # Inicia la aplicación Kivy
