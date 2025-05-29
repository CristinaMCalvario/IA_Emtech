from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.uix.scrollview import ScrollView
from tabulate import tabulate
from kivy.graphics import Color, Rectangle

# --------------------------- BASE DE DATOS -----------------------------------

def conectar_db():
    """Crea la base de datos y la tabla si no existen"""
    conn = sqlite3.connect('productos.db')  # Conecta a la base de datos SQLite
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL
        )
    ''')  # Crea la tabla productos si no existe
    conn.commit()
    conn.close()  # Cierra la conexión con la base de datos


def obtener_productos():
    """Consulta todos los productos de la base de datos"""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")  # Obtiene todos los productos
    productos = cursor.fetchall()
    conn.close()
    return productos


def agregar_producto(id_producto):
    """Agrega un producto al carrito basado en su ID"""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE id=?", (id_producto,))  # Obtiene el producto por ID
    producto = cursor.fetchone()
    if producto:
        carrito.append((id_producto, producto[0], producto[1]))  # Agrega (ID, nombre, precio) al carrito
    conn.close()


def eliminar_producto(id_producto):
    """Elimina un producto del carrito basado en su ID"""
    global carrito
    carrito = [item for item in carrito if item[0] != id_producto]  # Filtra el carrito sin el producto dado


def calcular_totales():
    """Calcula el total de productos y el pago total"""
    total_productos = len(carrito)
    total_pago = sum(float(producto[2]) for producto in carrito)  # Convierte el precio a float antes de sumarlo
    return total_productos, total_pago


# --------------------------- INTERFAZ GRÁFICA -----------------------------------
class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.orientation = 'vertical'

        # Fijar el color de fondo azul con Canvas
        with self.canvas.before:
            Color(0, 0, 1, 1)  # Azul
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        conectar_db()  # Asegura que la base de datos esté creada al iniciar la aplicación
        

 # ---------------- BOTÓN DEL CHATBOT ----------------
        chatbot_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.btn_chatbot = Button(
            text="Abrir Chatbot de Ayuda", 
            size_hint=(1, 1),
            background_color=(0.2, 0.8, 0.2, 1),  # Verde
            color=(1, 1, 1, 1)  # Texto blanco
        )
        self.btn_chatbot.bind(on_press=self.open_chatbot)
        chatbot_layout.add_widget(self.btn_chatbot)
        self.add_widget(chatbot_layout)


        # ---------------- SECCIÓN DE PRODUCTOS DISPONIBLES ----------------
        self.add_widget(Label(text="PRODUCTOS DISPONIBLES", font_size=24, size_hint_y=0.1, bold=True))  # Título
        
        self.product_list = ScrollView()  # Contenedor con desplazamiento para la lista de productos
        self.grid_layout = GridLayout(cols=3, spacing=5, padding=5, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Agregar encabezado de la tabla
        self.grid_layout.add_widget(Label(text="ID", size_hint_y=None, height=40, bold=True))  # Encabezado para ID
        self.grid_layout.add_widget(Label(text="Nombre", size_hint_y=None, height=40, bold=True))  # Encabezado para Nombre
        self.grid_layout.add_widget(Label(text="Precio", size_hint_y=None, height=40, bold=True))  # Encabezado para Precio
        
        self.actualizar_lista_productos()  # Cargar productos al iniciar la aplicación
        self.product_list.add_widget(self.grid_layout)  # Agregar los productos al contenedor de desplazamiento
        self.add_widget(self.product_list)  # Agregar el contenedor de productos a la interfaz

        # ---------------- SECCIÓN DE ACCIONES ----------------
        self.input_id = TextInput(hint_text="ID del Producto", size_hint_y=None, height=40)  # Campo de texto para capturar ID del producto
        self.btn_agregar = Button(text="Alta", size_hint_y=None, height=40, on_press=self.agregar_producto)  # Botón para agregar productos al carrito
        self.btn_eliminar = Button(text="Eliminar", size_hint_y=None, height=40, on_press=self.eliminar_producto)  # Botón para eliminar productos del carrito
        
        self.add_widget(self.input_id)  # Agregar el campo de texto a la interfaz
        self.add_widget(self.btn_agregar)  # Agregar el botón de alta
        self.add_widget(self.btn_eliminar)  # Agregar el botón de eliminar

        # ---------------- SECCIÓN DE TOTALES ----------------
        self.total_label = Label(text="Total productos: 0 | Total pago: $0.00", size_hint_y=None, height=40)  # Etiqueta para mostrar totales
        self.add_widget(self.total_label)  # Agregar la etiqueta de totales

        self.btn_consultar = Button(text="Consultar", size_hint_y=None, height=40, on_press=self.consultar_carrito)  # Botón para consultar el carrito
        self.add_widget(self.btn_consultar)  # Agregar el botón de consulta

        # Botón de "Productos Disponibles"
        self.btn_productos_disponibles = Button(text="Productos Disponibles", size_hint_y=None, height=40, on_press=self.mostrar_productos_disponibles)
        self.add_widget(self.btn_productos_disponibles)

    def update_rect(self, *args):
        """Actualizar la posición y tamaño del fondo azul cuando cambian las dimensiones de la ventana"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def actualizar_lista_productos(self):
        """Refresca la lista de productos en pantalla"""
        self.grid_layout.clear_widgets()  # Borra los productos actuales de la vista
        
        # Agregar encabezado de la tabla nuevamente
        self.grid_layout.add_widget(Label(text="ID", size_hint_y=None, height=40, bold=True))  # Encabezado para ID
        self.grid_layout.add_widget(Label(text="Nombre", size_hint_y=None, height=40, bold=True))  # Encabezado para Nombre
        self.grid_layout.add_widget(Label(text="Precio", size_hint_y=None, height=40, bold=True))  # Encabezado para Precio
        
        productos = obtener_productos()  # Obtiene la lista actualizada de productos

        for producto in productos:
            # Agregar un nuevo producto al listado
            self.grid_layout.add_widget(Label(text=str(producto[0]), size_hint_y=None, height=40))  # ID del producto
            self.grid_layout.add_widget(Label(text=producto[1], size_hint_y=None, height=40))  # Nombre del producto
            self.grid_layout.add_widget(Label(text=f"${float(producto[2]):.2f}", size_hint_y=None, height=40))  # Precio formateado a 2 decimales

    def agregar_producto(self, instance):
        """Lógica para agregar productos desde la interfaz"""
        id_producto = self.input_id.text.strip()
        
        if id_producto.isdigit():
            agregar_producto(int(id_producto))  # Agrega el producto al carrito
            self.input_id.text = ""  # Limpia el campo de entrada
            self.actualizar_totales()

    def eliminar_producto(self, instance):
        """Lógica para eliminar un producto"""
        id_producto = self.input_id.text.strip()
        
        if id_producto.isdigit():
            eliminar_producto(int(id_producto))  # Elimina el producto por ID
            self.input_id.text = ""  # Limpia el campo de entrada
            self.actualizar_totales()

    def actualizar_totales(self):
        """Actualiza los totales en la interfaz"""
        total_productos, total_pago = calcular_totales()
        self.total_label.text = f"Total productos: {total_productos} | Total pago: ${total_pago:.2f}"

    def consultar_carrito(self, instance):
        """Limpia los productos disponibles y muestra los productos agregados al carrito"""
        self.grid_layout.clear_widgets()  # Limpiar la vista de productos disponibles
        
        # Mostrar título para productos en carrito
        self.add_widget(Label(text="PRODUCTOS AGREGADOS AL CARRITO DE COMPRA", font_size=24, size_hint_y=None, height=40, bold=True))
        
        # Agregar encabezados para la tabla
        self.grid_layout.add_widget(Label(text="ID", size_hint_y=None, height=40, bold=True))  # Encabezado para ID
        self.grid_layout.add_widget(Label(text="Nombre", size_hint_y=None, height=40, bold=True))  # Encabezado para Nombre
        self.grid_layout.add_widget(Label(text="Precio", size_hint_y=None, height=40, bold=True))  # Encabezado para Precio

        # Mostrar productos del carrito con formato bonito
        for producto in carrito:
            self.grid_layout.add_widget(Label(text=str(producto[0]), size_hint_y=None, height=40))  # ID del producto
            self.grid_layout.add_widget(Label(text=producto[1], size_hint_y=None, height=40))  # Nombre del producto
            self.grid_layout.add_widget(Label(text=f"${float(producto[2]):.2f}", size_hint_y=None, height=40))  # Precio del producto
        
        self.actualizar_totales()

    def mostrar_productos_disponibles(self, instance):
        """Muestra la lista de productos disponibles nuevamente"""
        self.grid_layout.clear_widgets()  # Limpiar vista actual
        
        self.add_widget(Label(text="PRODUCTOS DISPONIBLES", font_size=24, size_hint_y=0.1, bold=True))  # Título
        self.actualizar_lista_productos()  # Mostrar productos disponibles nuevamente

    def open_chatbot(self, instance):
        """Abre el chatbot en el navegador predeterminado"""
        import webbrowser
        webbrowser.open("https://widget.kommunicate.io/chat?appId=1ef0018ec23321811284bcdb1b4194c87")

# --------------------------- EJECUCIÓN DE LA APP ---------------------------
class MyApp(App):
    def build(self):
        self.title = "CARRITO DE COMPRAS EN LINEA"  # Cambiar el título de la ventana
        return MainScreen()  # Devuelve la pantalla principal

if __name__ == '__main__':
    carrito = []  # Lista para almacenar los productos agregados
    MyApp().run()  # Ejecuta la aplicación