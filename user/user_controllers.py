from flask import request, jsonify
from user.user_model import User
from config.config import Config
from bson import ObjectId
from bson import json_util

bcrypt = Config.bcrypt
client = Config.client
db = Config.db

def register_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    existing_user = db.db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(username, password, email)
    db.db.users.insert_one({'username': new_user.username, 'password': new_user.password, 'email': new_user.email})

    return jsonify({'message': 'Registration successful'}), 201


def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = db.db.users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])

        # Remove the password field for security reasons
        user.pop('password', None)

        # Convert ObjectId to string in nested documents
        for plant in user.get('plants', []):
            plant['_id'] = str(plant.get('_id'))

        # Return the entire user object upon successful login
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401



def get_all_users():
    users = db.db.users.find()
    user_list = []
    for user in users:
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])
        
        # Remove the password field for security reasons
        user.pop('password', None)

        # Convert ObjectId to string in nested documents
        for plant in user.get('plants', []):
            plant['_id'] = str(plant.get('_id'))

        user_list.append(user)
    return jsonify({'users': user_list}), 200


def get_user_by_id(user_id):
    # Convert the user_id string to ObjectId
    user_id = ObjectId(user_id)
    user = db.db.users.find_one({'_id': user_id})
    if user:
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])

        # Remove the password field for security reasons
        user.pop('password', None)

        # Convert ObjectId to string in nested documents
        for plant in user.get('plants', []):
            plant['_id'] = str(plant.get('_id'))

        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

def delete_user_by_id(user_id):
    # Convert the user_id string to ObjectId
    user_id = ObjectId(user_id)
    user = db.db.users.find_one({'_id': user_id})
    if user:
        db.db.users.delete_one({'_id': user_id})
        return jsonify({'message': 'User deleted'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
def update_user_by_id(user_id):
    try:
        # Convert the user_id string to ObjectId
        user_id = ObjectId(user_id)
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        existing_user = db.db.users.find_one({'_id': user_id})
        if not existing_user:
            return jsonify({'error': 'User not found'}), 404

        update_data = {}
        if username:
            update_data['username'] = username
        if password:
            update_data['password'] = password
        if email:
            update_data['email'] = email

        db.db.users.update_one({'_id': user_id}, {'$set': update_data})
        return jsonify({'message': 'User updated'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid user ID format'}), 400