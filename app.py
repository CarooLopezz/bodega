from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.reception_routes import receptions 
from routes.user_routes import users        

# Importa todos los modelos aquí para que SQLAlchemy los registre
from models.reception import Reception
from models.user import User 

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(receptions)
app.register_blueprint(users) 

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    
    db.create_all() # Crea las tablas si no existen.

if __name__ == '__main__':
    app.run(debug=True)