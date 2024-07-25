from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    date_of_suscription = db.Column(db.Date, nullable=False)
    favorites = db.relationship('Favorites', backref='favorites_user', lazy=True)

    def __repr__(self):
            return f'Email: {self.email} - ID: {self.id}'

    def serialize(self):
            return {
                "id": self.id,
                "email": self.email,
                "name": self.name,
                "last_name": self.last_name,
                "date_of_suscription": self.date_of_suscription,
                # do not serialize the password, its a security breach
            }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
            return f'User Id: {self.user_id}'

    def serialize(self):
            return {
                "id": self.id,
                "user": self.user_id,
                "planet": self.planet_id,
                "vehicle": self.vehicle_id,
                "character": self.character_id,
            }
    
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    population = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    favorite = db.relationship('Favorites', backref='favorites_planet', lazy=True)

    def __repr__(self):
            return f'Name: {self.name}'

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "population": self.population,
                "diameter": self.diameter,
            }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', backref='favorites_vehicle', lazy=True)

    def __repr__(self):
            return f'Name: {self.name}'

    def serialize(self):
            return {
                "id": self.id,          
                "name": self.name,
                "model": self.model,
                "size": self.size,
            }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', backref='favorites_character', lazy=True)

    def __repr__(self):
            return f'Name: {self.name}'

    def serialize(self):
            return {
                "id": self.id,          
                "name": self.name,
                "gender": self.gender,
                "eye_color": self.eye_color,
            }

    