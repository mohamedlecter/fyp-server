from flask import Flask, jsonify
from flask_cors import CORS
from config.config import Config
from user.user_routes import user_bp
# from diagnose.diagnose_routes import diagnose_bp
from plant.plant_routes import plant_bp
from user_plants.user_plant_routes import user_plant_bp
from chatbot.chatbot_routes import chatbot_bp

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Initialize MongoDB client and Bcrypt
client = Config.client
db = Config.db
bcrypt = Config.bcrypt

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/user')
# app.register_blueprint(diagnose_bp, url_prefix='/diagnose')
app.register_blueprint(plant_bp, url_prefix='/plant')
app.register_blueprint(user_plant_bp, url_prefix='/user_plant')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Plant Disease Diagnosis API'})


if __name__ == '__main__':
    app.run(debug=True)

