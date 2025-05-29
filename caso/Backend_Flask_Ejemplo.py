from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

    # Aquí debes poner tu cadena de conexión a la base de datos
    # Asegúrate de que el puerto, usuario, contraseña y nombre de la base de datos sean correctos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/marketplace'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    # Para evitar una advertencia
   # inicializa una instancia de SQLAlchemy y la asocia con tu aplicación Flask 
db = SQLAlchemy(app)

    # Definición del modelo User (esto corresponde a la tabla ya existente en la base de datos), 
    # Define un modelo llamado User que hereda de db.Model, la clase base de SQLAlchemy para modelos. Esto indica que esta clase está vinculada a una tabla en la base de datos.
class User(db.Model):
        __tablename__ = 'users'
        UserID = db.Column(db.Integer, primary_key=True)  # Nombre correcto de la columna
        username = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(50), nullable=False)

        products = db.relationship('Product', backref='seller', lazy=True)
        orders = db.relationship('Order', backref='buyer', lazy=True)

    # Para inicializar la base de datos (si fuera necesario)
    # db.create_all()  # Descomenta esto solo si quieres crear las tablas (si no existen)
@app.route('/')
def home():
        return "¡La aplicación Flask está funcionando!"

    # Ruta de ejemplo para verificar que la conexión y los modelos funcionan
@app.route('/users', methods=['GET'])
def get_users():
        users = User.query.all()  # Obtiene todos los usuarios de la base de datos
        return jsonify([{'UserID': user.UserID, 'username': user.username, 'email': user.email} for user in users])

    # agregue HOY...
@app.route('/users', methods=['POST'])
def add_user():
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'email' not in data or 'password' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica

            new_user = User(
                UserID=data['UserID'],  # Ahora se toma el UserID del JSON  
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
    # AGREGUE HOY....
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'email' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica
            user = User.query.get_or_404(user_id)
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
           
            db.session.commit()
            return jsonify({"message": "Usuario actualizado con éxito"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
        
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
        user = User.query.get_or_404(user_id)  # Get user by ID, return 404 if not found

        try:
            db.session.delete(user)

            db.session.commit()
            return jsonify({"message": "Usuario eliminado con éxito"}), 200  # Successful deletion, no content to return
        except Exception as e:
            #db.session.rollback()
            return jsonify({'error': str(e)}), 500

#if __name__ == '__main__':
#        app.run(debug=True, port=5000)  # Aquí puedes cambiar el puerto si es necesario





#Set-ExecutionPolicy Unrestricted -Scope Process 
#Set-ExecutionPolicy Unrestricted -Scope Process
#venv\Scripts\activate
# Modelos de SQLAlchemy (User, Product, Order) aquí...
#Products

class Product(db.Model):
    __tablename__ = 'products'
    ProductID = db.Column(db.Integer, primary_key=True)
    SellerID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ProductName = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)

    # Relación con Order
    orders = db.relationship('Order', backref='product', lazy=True)

    # Para inicializar la base de datos (si fuera necesario)
    # db.create_all()  # Descomenta esto solo si quieres crear las tablas (si no existen)

@app.route('/products', methods=['GET'])
def get_products():
        products = Product.query.all()  # Obtiene todos los productos de la base de datos
        return jsonify([{'ProductID': product.ProductID, 'SellerID': product.SellerID, 'ProductName': product.ProductName, 'Description' : product.Description, 'Price' : product.Price} for product in products])

    # agregue HOY...
@app.route('/products', methods=['POST'])
def add_product():
        try:
            data = request.get_json()
            if not data or 'ProductName' not in data or 'Description' not in data or 'Price' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica

            new_product = Product(
                ProductID=data['ProductID'],  # Ahora se toma el UserID del JSON  
                SellerID=data['SellerID'],
                ProductName=data['ProductName'],
                Description=data['Description'],
                Price=data['Price']
            )
            db.session.add(new_product)
            db.session.commit()
            return jsonify({'message': 'Product added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
    # AGREGUE HOY....
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
        try:
            data = request.get_json()
            if not data or 'SellerID' not in data or 'ProductName' not in data or 'Description' not in data or 'Price' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica
            product = Product.query.get_or_404(product_id)
            data = request.get_json()
            product.SellerID = data['SellerID']
            product.ProductName = data['ProductName']
            product.Description = data['Description']
            product.Price = data['Price']
           
            db.session.commit()
            return jsonify({"message": "Producto actualizado con éxito"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
        
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
        product = Product.query.get_or_404(product_id)  # Get user by ID, return 404 if not found

        try:
            db.session.delete(product)

            db.session.commit()
            return jsonify({"message": "Producto eliminado con éxito"}), 200  # Successful deletion, no content to return
        except Exception as e:
            #db.session.rollback()
            return jsonify({'error': str(e)}), 500


#Orders
class Order(db.Model):
    __tablename__ = 'orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    BuyerID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    OrderDate = db.Column(db.DateTime, nullable=False)

@app.route('/orders', methods=['GET'])
def get_orders():
        orders = Order.query.all()  # Obtiene todos los ordenes de la base de datos
        return jsonify([{'OrderID': order.OrderID, 'BuyerID': order.BuyerID, 'ProductID': order.ProductID, 'Quantity' : order.Quantity, 'OrderDate' : order.OrderDate} for order in orders])

    # agregue HOY...
@app.route('/orders', methods=['POST'])
def add_order():
        try:
            data = request.get_json()
            if not data or 'Quantity' not in data or 'OrderDate' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica

            new_order = Order(
                OrderID=data['OrderID'],  # Ahora se toma el UserID del JSON
                BuyerID=data['BuyerID'],
                ProductID=data['ProductID'],
                Quantity=data['Quantity'],
                OrderDate=data['OrderDate']
            )

            db.session.add(new_order)
            db.session.commit()
            # db.session.commit()  # Guarda los cambios en la base de datos
            return jsonify({'message': 'Order added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
    # AGREGUE HOY....
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
        try:
            data = request.get_json()
            if not data or 'Quantity' not in data or 'OrderDate' not in data:
                return jsonify({'error': 'Invalid input'}), 400  # Validación básica
            order = Order.query.get_or_404(order_id)
            data = request.get_json()
            order.BuyerID = data['BuyerID']
            order.ProductID = data['ProductID']
            order.Quantity = data['Quantity']
            order.OrderDate = data['OrderDate']
           
            db.session.commit()
            return jsonify({"message": "Orden actualizado con éxito"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Captura errores
        
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
        order = Order.query.get_or_404(order_id)  # Get user by ID, return 404 if not found

        try:
            db.session.delete(order)

            db.session.commit()
            return jsonify({"message": "Orden eliminado con éxito"}), 200  # Successful deletion, no content to return
        except Exception as e:
            #db.session.rollback()
            return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
        app.run(debug=True, port=5000)