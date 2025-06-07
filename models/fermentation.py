import uuid
from models.db import db

class FermentationProcess(db.Model):
    __tablename__ = 'fermentation_process'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    productName = db.Column(db.String(50), unique=True, nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pH = db.Column(db.Float, nullable=True)
    acidity = db.Column(db.Float, nullable=True)  # Se agregó acidez
    status = db.Column(db.Boolean, default=True)

    def __init__(self, productName, startDate, temperature, pH=None, acidity=None, status=True):
        self.productName = productName
        self.startDate = startDate
        self.temperature = temperature
        self.pH = pH
        self.acidity = acidity
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'startDate': self.startDate,
            'temperature': self.temperature,
            'pH': self.pH,
            'acidity': self.acidity,
            'status': self.status
        }