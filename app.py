from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db

# --- COMBINACIÓN DE IMPORTS DE BLUEPRINTS ---
from routes.wines_routes import wines
from routes.reception_routes import receptions
from routes.user_routes import users

# --- COMBINACIÓN DE IMPORTS DE MODELOS ---
from models.wines import Wines 
from models.reception import Reception
from models.user import User

app = Flask(__name__)

app.secret_key = 'clave_secreta'
app.register_blueprint(wines) 

app.register_blueprint(receptions)
app.register_blueprint(users)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config["TEMPLATES_AUTO_RELOAD"] = True 

db.init_app(app)

with app.app_context():
    # db.drop_all() #  Si quieres conservar datos, esta línea DEBE estar comentada.
    db.create_all() 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003,debug=True)