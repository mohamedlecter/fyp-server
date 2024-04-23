from flask import Blueprint, jsonify, request
from user_plants.user_plants_controllers import add_plant, delete_plant

user_plant_bp = Blueprint("user_plant", __name__)

@user_plant_bp.route('/add_plant', methods=['POST'])
def add():
     # Extract user_id and plant_id from request
    user_id = request.json.get('user_id')
    plant_id = request.json.get('plant_id')
    
    # Check if both user_id and plant_id are provided
    if not user_id or not plant_id:
        return jsonify({'error': 'User ID and Plant ID are required'}), 400
    
    
    return add_plant(user_id, plant_id)

@user_plant_bp.route('/delete_plant', methods=['DELETE'])
def delete():
    # Extract user_id and plant_id from request
    user_id = request.json.get('user_id')
    plant_id = request.json.get('plant_id')
    
    # Check if both user_id and plant_id are provided
    if not user_id or not plant_id:
        return jsonify({'error': 'User ID and Plant ID are required'}), 400
    
    return delete_plant(user_id, plant_id)
