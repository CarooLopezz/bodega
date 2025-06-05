from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.wines_routes import wines
from models.wines import Wines
app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(wines)



app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

db.init_app(app)

with app.app_context():
    from models.wines import Wines
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003,debug=True)