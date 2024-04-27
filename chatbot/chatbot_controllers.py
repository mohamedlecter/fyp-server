import os
from openai import OpenAI
from config.config import Config

# Initialize MongoDB client
client = Config.client
db = Config.db
chat_collection = db.db.chats


# Initialize OpenAI client with API key
client = OpenAI(
    api_key="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",
)

def chatbot(user_id, user_message):
    # Retrieve or create a chat document for the user
    chat_document = chat_collection.find_one({"user_id": user_id})
    if chat_document is None:
        # Create a new chat document
        chat_document = {"user_id": user_id, "conversation_history": []}
        chat_collection.insert_one(chat_document)

    # Define the conversation messages
    messages = [{"role": "user", "content": user_message}]

    # Generate a completion using the chat model
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages  # Include user's previous messages in the conversation
    )

    # Extract bot's response
    bot_reply = completion.choices[0].message.content

    # Add the user's message and bot's reply to the conversation history
    chat_document['conversation_history'].extend(messages)
    chat_document['conversation_history'].append({"role": "system", "content": bot_reply})
    
    # Update chat document in MongoDB with the updated conversation history
    chat_collection.update_one({"user_id": user_id}, {"$set": {"conversation_history": chat_document['conversation_history']}})

    return bot_reply

# Function to get all conversations with a specific user
def get_user_conversations(user_id):
    # Retrieve all chat documents for the user
    user_conversations = chat_collection.find({"user_id": user_id})

    # Initialize list to store conversation histories
    conversations = []

    # Iterate over chat documents and extract conversation histories
    for chat_document in user_conversations:
        conversations.append({
            "conversation_id": str(chat_document['_id']),
            "conversation_history": chat_document['conversation_history']
        })

    return conversations
