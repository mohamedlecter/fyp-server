from flask import request, jsonify
from user.user_model import User
from config.config import Config
from bson import ObjectId

bcrypt = Config.bcrypt
client = Config.client
db = Config.db

def add_plant(user_id, plant_id):
    user = db.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        plant = db.db.plants.find_one({'_id': ObjectId(plant_id)})
        if plant:
            db.db.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'plants': plant}})
            return jsonify({'message': 'Plant added to user collection'}), 200
        else:
            return jsonify({'error': 'Plant not found'}), 404
    else:
        return jsonify({'error': 'User not found'}), 404


