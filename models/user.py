import uuid
from models.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    username = db.Column(db.String(50), nullable=False) 
    
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')

    def __init__(self, username, email, password_hash, role='user'): # role con valor por defecto
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role 
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username, 
            'email': self.email,
            'role': self.role
        }