# app.py
from flask import Flask
from flask import jsonify
from models import db  # Ahora importamos db desde models
from models import User  # Esta importación ahora es segura

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos db con la aplicación
db.init_app(app)

# Importar los modelos al final para evitar circular imports
from models import User

# Ruta de ejemplo para crear usuarios
@app.route('/users', methods=['POST'])
def create_user():
    from flask import request
    data = request.json
    
    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password')  # En producción esto debería estar hasheado
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return {
        'message': 'Usuario creado con éxito',
        'user_id': new_user.id
    }, 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []
            
    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
         # No incluir la contraseña por seguridad
        })
            
    return jsonify({'users': users_list, 'count': len(users_list)}), 200

if __name__ == '__main__':
    app.run(debug=True)