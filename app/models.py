# app/models.py
# from app import db
# from flask_login import UserMixin


from app.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # is_active = False  # Active by default
    # Required properties and methods for Flask-Login
    @property
    def is_authenticated(self):
        return True
    
    @is_authenticated.setter
    def is_authenticated(self, value):
        self.is_authenticated = value

    @property
    def is_active(self):
        return True
    
    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def is_anonymous(self):
        return False
    
    @is_anonymous.setter
    def is_anonymous(self, value):
        self.is_anonymous = value

    def get_id(self):
        return str(self.id)
    
class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_active = False  # Active by default