from models.db import db
import uuid
from datetime import datetime

class Reception(db.Model):
    __tablename__ = 'receptions'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variety = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    acidity = db.Column(db.Float, nullable=False)
    pH = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

    def calculate_maturity(self):
        if self.acidity < 3.5 and self.pH > 3.2:
            return "Maduro"
        return "Verde"
