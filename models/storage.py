import uuid
from models.db import db

class StorageProcess(db.Model):
    __tablename__ = 'storage_process'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    productName = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Ubicación de almacenamiento
    conditions = db.Column(db.Text, nullable=True)  # Condiciones de almacenamiento
    capacity = db.Column(db.Integer, nullable=False)  # Capacidad en unidades
    status = db.Column(db.Boolean, default=True)

    def __init__(self, productName, location, capacity, conditions=None, status=True):
        self.productName = productName
        self.location = location
        self.capacity = capacity
        self.conditions = conditions
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'location': self.location,
            'conditions': self.conditions,
            'capacity': self.capacity,
            'status': self.status
        }