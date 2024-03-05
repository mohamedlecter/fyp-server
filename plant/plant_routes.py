import re
from flask import Blueprint, jsonify
from plant.plant_controller import get_plants, get_plant_by_id, upload_file,find_plant_by_disease, get_random_plants, search_plants_by_name
import os


file = os.path.abspath("server\data.json")

plant_bp = Blueprint("plant", __name__)

@plant_bp.route('/', methods=['GET'])
def plants():
    return get_plants()

@plant_bp.route('/<plant_id>', methods=['GET'])
def plant_by_id(plant_id):
    return get_plant_by_id(plant_id)

@plant_bp.route('/random', methods=['GET'])
def random_plants():
    return get_random_plants() 

@plant_bp.route('/search/<plant_name>', methods=['GET'])
def search_plants(plant_name):
    return search_plants_by_name(plant_name)

@plant_bp.route('/disease/<disease_name>', methods=['GET'])
def plant_by_disease(disease_name):
    return find_plant_by_disease(disease_name)

@plant_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    return upload_file(file)

