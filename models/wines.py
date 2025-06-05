import uuid
from models.db import db

class Wines(db.Model):
    __tablename__ = 'wines'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))# librería que genera el id ,lambda es una función
    name = db.Column(db.String(50), unique=True, nullable=False)
    origen = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    
    def __init__(self,name,origen, image):
        self.name = name
        self.origen = origen
        self.image =image

    
    

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'origen': self.origen,
            'image': self.image,
        }

   