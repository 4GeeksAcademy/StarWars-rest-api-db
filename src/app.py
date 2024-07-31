"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Favorites, Planet, Vehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Este Endpoint lista todos los usuarios del blog
@app.route('/all_users', methods=['GET'])
def get_all_users():
    users= User.query.all()
    if users == None:
        return jsonify({"msg": "Users not found"}), 404
    else:
        users_serialized =  list(map(lambda item: item.serialize(), users))
        return jsonify(users_serialized), 200

#Este Endpoint obtiene todos los personajes
@app.route('/all_characters', methods=['GET'])
def get_all_characters():
    characters= Character.query.all()
    if characters == None:
        return jsonify({"msg": "Characters not found"}), 404
    else:
        characters_serialized =  list(map(lambda item: item.serialize(), characters))
        return jsonify(characters_serialized), 200

#Este Endpoint obtiene 1 personaje
@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character= Character.query.filter_by(id=id).first()
    if character == None:
        return jsonify({"msg": "Character not found"}), 404
    else:
        character_serialized = character.serialize()
        return jsonify(character_serialized), 200
       
#Este Endpoint obtiene todos los planetas
@app.route('/all_planets', methods=['GET'])
def get_all_planets():
    planets= Planet.query.all()
    if planets == None:
        return jsonify({"msg": "Planets not found"}), 404
    else:
        planets_serialized =  list(map(lambda item: item.serialize(), planets))
        return jsonify(planets_serialized), 200
    
#Este Endpoint obtiene 1 planeta
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet= Planet.query.filter_by(id=id).first()
    if planet == None:
        return jsonify({"msg": "Planet not found"}), 404
    else:
        planet_serialized = planet.serialize()
        return jsonify(planet_serialized), 200
    
#Este Endpoint obtiene todos los vehiculos
@app.route('/all_vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles= Vehicle.query.all()
    if vehicles == None:
        return jsonify({"msg": "Vehicles not found"}), 404
    else:
        vehicles_serialized =  list(map(lambda item: item.serialize(), vehicles))
        return jsonify(vehicles_serialized), 200
    
#Este Endpoint obtiene 1 vehiculo
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_one_vehicle(id):
    vehicle= Planet.query.filter_by(id=id).first()
    if vehicle == None:
        return jsonify({"msg": "Vehicle not found"}), 404
    else:
        vehicle_serialized = vehicle.serialize()
        return jsonify(vehicle_serialized), 200

#Este Endpoint obtiene los favoritos de cada usuario por ID
@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):
    favorites= Favorites.query.filter_by(user_id= id).all()
    if favorites == []:
        return jsonify({"msg": "Favorites not found"}), 404
    else:
        favorite_serialized = list(map(lambda item: item.serialize(), favorites))
        return jsonify(favorite_serialized), 200
    
#Este Endpoint Elimina un planet favorito con el id 
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>/', methods=['DELETE'])
def delete_planet_favorite(planet_id, user_id):
    favorite= Favorites.query.filter_by(user_id= user_id, planet_id= planet_id).first()
    if favorite == None:
        return jsonify({"msg": "Favorites not found"}), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite has been deleted"}), 200

#Este Endpoint Elimina un personaje favorito con el id 
@app.route('/favorite/user/<int:user_id>/character/<int:character_id>/', methods=['DELETE'])
def delete_character_favorite(character_id, user_id):
    favorite= Favorites.query.filter_by(user_id= user_id, character_id= character_id).first()
    if favorite == None:
        return jsonify({"msg": "Favorites not found"}), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite has been deleted"}), 200

#Este Endpoint añade un nuevo personaje favorito al usuario actual con el id = character_id
@app.route('/favorite/user/<int:user_id>/character/<int:character_id>/', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if not user or not character:
        return jsonify({"msg": "User or character not found"}), 404
    else:
        new_favorite_character = Favorites(user_id = user_id, character_id = character_id)
        db.session.add(new_favorite_character)
        db.session.commit()
    return jsonify(new_favorite_character.serialize()), 200

#Este Endpoint añade un nuevo planeta favorito al usuario actual con el id = planet_id
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>/', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"msg": "User or planet not found"}), 404
    else:
        new_favorite_planet = Favorites(user_id = user_id, planet_id = planet_id)
        db.session.add(new_favorite_planet)
        db.session.commit()
    return jsonify(new_favorite_planet.serialize()), 200

#Este Endpoint crea un nuevo PERSONAJE
@app.route('/new_character', methods=['POST'])
def post_character():
    character = request.get_json()
    if not isinstance(character['name'], str) or len(character['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(character['gender'], str) or len(character['gender'].strip()) == 0:
         return({'error':'"gender" must be a string'}), 400
    if not isinstance(character['eye_color'], str) or len(character['eye_color'].strip()) == 0:
         return({'error':'"eye_color" must be a string'}), 400
    character_created = Character(name=character['name'],gender=character['gender'],eye_color=character['eye_color'])
    db.session.add(character_created)
    db.session.commit()
    return jsonify('Character added'), 200

#Este Endpoint crea un nuevo PLANETA
@app.route('/new_planet', methods=['POST'])
def post_planet():
    planet = request.get_json()
    if not isinstance(planet['name'], str) or len(planet['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(planet['population'], str) or len(planet['population'].strip()) == 0:
         return({'error':'"population" must be a string'}), 400
    if not isinstance(planet['diameter'], str) or len(planet['diameter'].strip()) == 0:
         return({'error':'"diameter" must be a string'}), 400
    planet_created = Planet(name=planet['name'],population=planet['population'],diameter=planet['diameter'])
    db.session.add(planet_created)
    db.session.commit()
    return jsonify('Planet added'), 200

#Este Endpoint crea un nuevo VEHÍCULO
@app.route('/new_vehicle', methods=['POST'])
def post_vehicle():
    vehicle = request.get_json()
    if not isinstance(vehicle['name'], str) or len(vehicle['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(vehicle['model'], str) or len(vehicle['model'].strip()) == 0:
         return({'error':'"model" must be a string'}), 400
    if not isinstance(vehicle['size'], str) or len(vehicle['size'].strip()) == 0:
         return({'error':'"size" must be a string'}), 400
    vehicle_created = Vehicle(name=vehicle['name'],model=vehicle['model'],size=vehicle['size'])
    db.session.add(vehicle_created)
    db.session.commit()
    return jsonify('Vehicle added'), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
