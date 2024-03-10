import json
import os
from bson import ObjectId
from flask import Flask, request, jsonify
import csv
from config.config import Config


bcrypt = Config.bcrypt
client = Config.client
db = Config.db

def get_plants():
    plants = db.db.plants.find()
    plants_list = []
    for plant in plants:
        plants_list.append({
            'id': str(plant['_id']),
            "title": plant.get("title", ""),
            "description": plant.get("description", ""),
            "scientific_name": plant.get("scientific_name", ""),
            "image": plant.get("image", ""),
            "uses": plant.get("uses", ""),
            "basic_requirements": plant.get("basic_requirements", ""),
            "growing": plant.get("growing", ""),
            "care": plant.get("care", ""),
            "harvesting": plant.get("harvesting", ""),
            "diseases": plant.get("diseases", [])
        })
    return jsonify(plants_list), 200

def get_random_plants():
    plants = db.db.plants.aggregate([{ '$sample': { 'size': 10 } }])
    plants_list = []
    for plant in plants:
        plants_list.append({
            'id': str(plant['_id']),
            "title": plant.get("title", ""),
            "description": plant.get("description", ""),
            "scientific_name": plant.get("scientific_name", ""),
            "image": plant.get("image", ""),
            "uses": plant.get("uses", ""),
            "basic_requirements": plant.get("basic_requirements", ""),
            "growing": plant.get("growing", ""),
            "care": plant.get("care", ""),
            "harvesting": plant.get("harvesting", ""),
            "diseases": plant.get("diseases", [])
        })
    return jsonify(plants_list), 200

def get_plant_by_id(plant_id):
    plant = db.db.plants.find_one({"_id": ObjectId(plant_id)})
    if plant:
        return jsonify({
            "id": str(plant['_id']),
            "topic_questions": plant.get("topic_questions", ""),
            "summary": plant.get("summary", ""),
            "image": plant.get("image", ""),
            "link_underline": plant.get("link-underline", ""),
            "link": plant.get("link", ""),
            "title": plant.get("title", ""),
            "description": plant.get("description", ""),
            "scientific_name": plant.get("scientific_name", ""),
            "common_name": plant.get("common_name:", ""), 
            "uses": plant.get("uses", ""),
            "basic_requirements": plant.get("basic_requirements", ""),
            "growing": plant.get("growing", ""),
            "care": plant.get("care", ""),
            "harvesting": plant.get("harvesting", ""),
            "diseases": plant.get("diseases", [])
        }), 200
    else:
        return jsonify({"error": "Plant not found"})
    
def search_plants_by_name(plant_name):
    plants = db.db.plants.find({"title": {"$regex": plant_name, "$options": "i"}})
    plants_list = []
    for plant in plants:
        plants_list.append({
            'id': str(plant['_id']),
            "title": plant.get("title", ""),
            "description": plant.get("description", ""),
            "scientific_name": plant.get("scientific_name", ""),
            "image": plant.get("image", ""),
            "uses": plant.get("uses", ""),
            "basic_requirements": plant.get("basic_requirements", ""),
            "growing": plant.get("growing", ""),
            "care": plant.get("care", ""),
            "harvesting": plant.get("harvesting", ""),
            "diseases": plant.get("diseases", [])
        })
    return jsonify(plants_list), 200
    

def find_plant_by_disease(disease_name):
    plants = db.db.plants.find()
    found_plants = []
    
    for plant in plants:
        matching_disease = None
        other_diseases = []
        for disease in plant.get("diseases", []):
            if disease.get("name") == disease_name:
                matching_disease = disease
            else:
                other_diseases.append(disease)
        
        if matching_disease or other_diseases:
            found_plants.append({
                'id': str(plant['_id']),
                "title": plant.get("title", ""),
                "description": plant.get("description", ""),
                "scientific_name": plant.get("scientific_name", ""),
                "image": plant.get("image", ""),
                "uses": plant.get("uses", ""),
                "basic_requirements": plant.get("basic_requirements", ""),
                "growing": plant.get("growing", ""),
                "care": plant.get("care", ""),
                "harvesting": plant.get("harvesting", ""),
                "matching_disease": matching_disease,
                "other_diseases": other_diseases
            })
    return jsonify(found_plants), 200


def upload_file(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': f"File '{file_path}' not found."})

        # Open the JSON file
        with open(file_path, 'r', encoding="utf8") as json_file:
            # Load JSON data from the file
            json_data = json.load(json_file)

            # Insert data into MongoDB collection
            db.db.plants.insert_many(json_data)

            return jsonify({'success': True, 'message': 'JSON data inserted to MongoDB'})
    except json.JSONDecodeError:
        return jsonify({'error': 'JSON decode error. The file might be empty or not in valid JSON format.'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
def get_user_plants(user_id):
    user = db.db.users.find_one({"_id": ObjectId(user_id)})

    if user:
        user_plants = user.get("plants", [])

        plants_list = []
        for plant in user_plants:
            plants_list.append({
                'id': str(plant['_id']),
                "title": plant.get("title", ""),
                "description": plant.get("description", ""),
                "scientific_name": plant.get("scientific_name", ""),
                "image": plant.get("image", ""),
                "uses": plant.get("uses", ""),
                "basic_requirements": plant.get("basic_requirements", ""),
                "growing": plant.get("growing", ""),
                "care": plant.get("care", ""),
                "harvesting": plant.get("harvesting", ""),
                "diseases": plant.get("diseases", [])
            })

        return jsonify(plants_list), 200
    else:
        return jsonify({"error": "User not found"}), 404
