# app/chatbot/chatbot_routes.py
from flask import Blueprint, request, jsonify
from chatbot.chatbot_controllers import chatbot

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']

    # Call the chatbot controller to generate a response
    bot_reply = chatbot(user_message)

    # Return the bot's response
    return jsonify({'message': bot_reply})
