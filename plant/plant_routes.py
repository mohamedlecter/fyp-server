import os
from flask import Blueprint, jsonify
from plant.plant_controller import get_plants, get_plant_by_id, upload_file, find_plant_by_disease, get_random_plants, search_plants_by_name, get_user_plants, get_user_plant, add_care_reminder, get_user_reminder_dates, get_user_reminder_dates_by_date
from bson import ObjectId
from datetime import datetime

file = os.path.abspath("data.json")

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

@plant_bp.route('/user/<user_id>', methods=['GET'])
def user_plants(user_id):
    return get_user_plants(user_id)

@plant_bp.route('/user/<user_id>/<plant_id>', methods=['GET'])
def user_plant_by_id(user_id, plant_id):
    return get_user_plant(user_id, plant_id)

@plant_bp.route('/search/<plant_name>', methods=['GET'])
def search_plants(plant_name):
    return search_plants_by_name(plant_name)

@plant_bp.route('/user/<user_id>/<plant_id>/care_reminders', methods=['POST'])
def add_reminder(user_id, plant_id):
    return add_care_reminder(user_id, plant_id)

@plant_bp.route('/user/<user_id>/reminder_dates', methods=['GET'])
def get_reminder_dates(user_id):
    return get_user_reminder_dates(user_id)

@plant_bp.route('/user/<user_id>/reminder_dates/<date>', methods=['GET'])
def get_reminder_dates_by_date(user_id, date):
    try:
        return get_user_reminder_dates_by_date(user_id, date)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400


@plant_bp.route('/disease/<disease_name>', methods=['GET'])
def plant_by_disease(disease_name):
    return find_plant_by_disease(disease_name)

@plant_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    return upload_file(file)
