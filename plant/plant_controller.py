import json
import os
from bson import ObjectId
from flask import Flask, request, jsonify
import csv
from config.config import Config
import re
from datetime import datetime

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
        return jsonify({"error": "Plant not found"}), 404
    
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
    # Check if the disease name contains "healthy"
    if "healthy" in disease_name:
        # Query the plant collection to find information about the plant itself
        plant_info = db.db.plants.find_one({"title": disease_name.split("__")[0]})
        if plant_info:
            return jsonify({
                'id': str(plant_info['_id']),
                "title": plant_info.get("title", ""),
                "description": plant_info.get("description", ""),
                "scientific_name": plant_info.get("scientific_name", ""),
                "image": plant_info.get("image", ""),
                "uses": plant_info.get("uses", ""),
                "basic_requirements": plant_info.get("basic_requirements", ""),
                "growing": plant_info.get("growing", ""),
                "care": plant_info.get("care", ""),
                "harvesting": plant_info.get("harvesting", ""),
                "diseases": plant_info.get("diseases", [])
            }), 200
        else:
            return jsonify({"error": "Plant not found"}), 404
    else:
        # Query the disease collection as before
        plants = db.db.plants.find({"diseases.name": {"$regex": disease_name, "$options": "i"}})
        plants_list = []
        for plant in plants:
            found_diseases = []
            other_diseases = []
            for disease in plant.get("diseases", []):
                if disease_name.lower() in disease["name"].lower():
                    found_diseases.append({
                        "category": disease.get("category", ""),
                        "cause": disease.get("cause", ""),
                        "comments": disease.get("comments", ""),
                        "name": disease.get("name", ""),
                        "symptoms": disease.get("symptoms", ""),
                        "treatment": disease.get("treatment", "")
                    })
                else:
                    other_diseases.append({
                        "category": disease.get("category", ""),
                        "cause": disease.get("cause", ""),
                        "comments": disease.get("comments", ""),
                        "name": disease.get("name", ""),
                        "symptoms": disease.get("symptoms", ""),
                        "treatment": disease.get("treatment", "")
                    })
            plants_list.append({
                "found_diseases": found_diseases,
                "other_diseases": other_diseases
            })
        return jsonify(plants_list), 200


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
                "diseases": plant.get("diseases", []),
                "care_reminders": plant.get("care_reminders", [])
                
            })

        return jsonify(plants_list), 200
    else:
        return jsonify({"error": "User not found"}), 404


def get_user_plant(user_id, plant_id):
    user = db.db.users.find_one({"_id": ObjectId(user_id)})
    
    if user:
        plant = next((plant for plant in user.get("plants", []) if str(plant['_id']) == plant_id), None)
        
        if plant:
            return jsonify({
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
                "diseases": plant.get("diseases", []),
                "care_reminders": plant.get("care_reminders", []),
                "completed": plant.get("completed", False),
                
            }), 200
        else:
            return jsonify({"error": "Plant not found for the user"}), 404
    else:
        return jsonify({"error": "User not found"}), 404
    
def add_care_reminder(user_id, plant_id):
    # Extract care reminder data from request body
    reminder_data = request.json
    action = reminder_data.get('action')
    time = reminder_data.get('time')
    
    try:
        # Check if the plant exists
        plant = db.db.users.find_one({"_id": ObjectId(user_id), "plants._id": ObjectId(plant_id)})
        if plant:
            # Add the care reminder to the plant's care_reminders array
            db.db.users.update_one(
                {"_id": ObjectId(user_id), "plants._id": ObjectId(plant_id)},
                {"$push": {"plants.$.care_reminders": {"action": action, "time": time, "completed": False}}},            )
            return jsonify({"success": True, "message": "Care reminder added successfully"}), 200
        else:
            # Add the plant and then add the care reminder
            db.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"plants": {"_id": ObjectId(plant_id), "care_reminders": [{"action": action, "time": time, "completed": False}]}}},            )
            return jsonify({"success": True, "message": "Plant and care reminder added successfully"}), 200
    except Exception as e:
        # Log the error
        print(f"Error in add_care_reminder: {e}")
        return jsonify({"error": str(e)}), 500
    
def get_user_reminder_dates(user_id):
    user = db.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        reminder_dates = {}
        for plant in user.get("plants", []):
            plant_id = str(plant["_id"])
            reminders = [{"action": reminder["action"], "time": reminder["time"]} for reminder in plant.get("care_reminders", []) if isinstance(reminder, dict)]
            for reminder in reminders:
                if plant_id not in reminder_dates:
                    reminder_dates[plant_id] = {"plant_id": plant_id, "title": plant.get("title", ""),"image": plant.get("image", ""),"actions": [reminder]}
                else:
                    reminder_dates[plant_id]["actions"].append(reminder)
        return jsonify({"reminder_dates": list(reminder_dates.values())}), 200
    else:
        return jsonify({"error": "User not found"}), 404

def get_user_reminder_dates_by_date(user_id, date_str):
    try:
        # Convert date string to datetime object
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        user = db.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            reminder_dates = {}
            for plant in user.get("plants", []):
                plant_id = str(plant["_id"])
                reminders = [{"action": reminder["action"], "time": reminder["time"], "completed": reminder.get("completed", False)} for reminder in plant.get("care_reminders", []) if isinstance(reminder, dict)]
                for reminder in reminders:
                    # Ensure reminder["time"] is a string before parsing
                    reminder_time_str = str(reminder["time"])
                    # Extract date from reminder's time as string
                    reminder_date = datetime.strptime(reminder_time_str[:10], "%Y-%m-%d").date()
                    # Convert date to string for comparison
                    reminder_date_str = reminder_date.strftime("%Y-%m-%d")
                    # Compare only the date part
                    if reminder_date_str == date_str:
                        if plant_id not in reminder_dates:
                            reminder_dates[plant_id] = {"plant_id": plant_id, "title": plant.get("title", ""),"image": plant.get("image", ""),"actions": [reminder]}
                        else:
                            reminder_dates[plant_id]["actions"].append(reminder)
            return jsonify({"reminder_dates": list(reminder_dates.values())}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        # Log the error
        print(f"Error in get_user_reminder_dates_by_date: {e}")
        return jsonify({"error": str(e)}), 500


def update_reminder_completion(user_id, plant_id, action, completed):
    user = db.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for plant in user.get("plants", []):
            if str(plant["_id"]) == plant_id:
                for reminder in plant.get("care_reminders", []):
                    if reminder.get("action") == action:
                        reminder["completed"] = completed
                        db.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"plants.$[p].care_reminders": plant["care_reminders"]}}, array_filters=[{"p._id": plant["_id"]}])
                        return jsonify({"message": "Reminder completion status updated successfully"}), 200
        return jsonify({"error": "Plant or reminder not found for the user"}), 404
    else:
        return jsonify({"error": "User not found"}), 404