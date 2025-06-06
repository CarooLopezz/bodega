import uuid
from models.db import db
from datetime import datetime

class Reception(db.Model):
    __tablename__ = 'receptions'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variety = db.Column(db.String(100), nullable=True)
    start_reception = db.Column (db.Datetime, nullable = True)
    end_reception = db.Column (db.Datetime, nullable = True)
    weight = db.Column(db.Float, nullable=True)
    acidity = db.Column(db.Float, nullable=True)
    ph = db.Column(db.Float, nullable=True)

def __init___ (self, variety,star_reception,end_reception, weight,acidity,ph):
    self.variety = variety
    self.start_reception = star_reception
    self.end_reception = end_reception
    self.weight = weight
    self.acidty = acidity
    self.ph = ph

def serialize (self,id,variety,start_reception,end_reception,weigth,acidity,ph):
    return {
    'id' : self.id,
    'variety' : self.variety,
    'start_reception': self.start_reception.strftime("%Y-%m-%d"), 
    'end_reception': self.end_reception.strftime("%Y-%m-%d"),
    'weight' : self.weight,
    'acidity' : self.acidity,
    'ph' : self.ph
    }
    

