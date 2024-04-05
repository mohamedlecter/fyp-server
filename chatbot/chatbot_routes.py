# app/chatbot/chatbot_routes.py
from flask import Blueprint, request, jsonify
from chatbot.chatbot_controllers import chatbot, get_user_conversations

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data['user_id']
    user_message = data['message']
    
    # Validate user input
    if not user_id or not user_message:
        return jsonify({"error": "Missing user_id or message in request"}), 400

    # Call the chatbot controller to generate a response
    bot_reply = chatbot(user_id, user_message)

    # Return the bot's response
    return jsonify({'message': bot_reply}), 200

@chatbot_bp.route('/chat/<user_id>', methods=['GET'])
def user_conversations(user_id):
    # Retrieve all conversations for the user
    conversations = get_user_conversations(user_id)
    
    # Return the conversations as JSON response
    return jsonify({"conversations": conversations}), 200
