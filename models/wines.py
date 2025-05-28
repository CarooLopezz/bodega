import uuid
from models.db import db

class Wines(db.Model):
    __tablename__ = 'vinos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))# librería que genera el id ,lambda es una función
    def __init__(self, productName,origen, imagen=None):
        self.productName = productName
        self.origen = origen
        self.imagen =imagen

    def serialize(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'origen': self.origen,
            'imagen': self.imagen,
        }

   