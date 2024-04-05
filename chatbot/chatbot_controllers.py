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
    
    # Define the conversation messages focusing on plant-related queries
    messages = [
        {"role": "system", "content": "Welcome to the Plant Assistant Bot! I'm here to help you with plant-related queries."},
        {"role": "user", "content": user_message}
    ]

    # Generate a completion using the chat model
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages= messages  # Include user's previous messages in the conversation
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


# # Initialize evaluation metrics
# total_responses = 0
# relevant_responses = 0
# accurate_completions = 0
# total_interactions = 0
# errors = 0
# successful_task_completions = 0
# total_tasks = 0

# def chatbot(user_message):
#     global total_responses, relevant_responses, accurate_completions, total_interactions, errors, successful_task_completions, total_tasks

#     # Increment total interactions
#     total_interactions += 1

#     # Define the conversation messages focusing on plant-related queries
#     messages = [
#         {"role": "system", "content": "Welcome to the Plant Assistant Bot! I'm here to help you with plant-related queries."},
#         {"role": "user", "content": user_message}
#     ]

#     # Generate a completion using the chat model
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo-0613",
#         messages=messages
#     )

#     # Extract bot's response
#     bot_reply = completion.choices[0].message.content

#     # Increment total responses
#     total_responses += 1

#     # Evaluate response relevance
#     if is_response_relevant(bot_reply):
#         relevant_responses += 1

#     # Evaluate completion accuracy
#     if is_completion_accurate(completion):
#         accurate_completions += 1

#     # Evaluate error rate
#     if is_error_present(bot_reply):
#         errors += 1

#     # Update task completion metrics (if applicable)
#     # For demonstration purposes, let's assume a specific task: "Identifying plant species"
#     total_tasks += 1
#     if is_task_completed(bot_reply):
#         successful_task_completions += 1

#     return bot_reply

# def is_response_relevant(response):
#     # Implement logic to determine relevance of response
#     # For simplicity, let's assume all responses are relevant
#     return True

# def is_completion_accurate(completion):
#     # Implement logic to determine accuracy of completion
#     # For simplicity, let's assume all completions are accurate
#     return True

# def is_error_present(response):
#     # Implement logic to determine if error is present in response
#     # For simplicity, let's assume there are no errors
#     return False

# def is_task_completed(response):
#     # Implement logic to determine if a specific task is completed based on response
#     # For demonstration purposes, let's assume the task is completed if the bot provides a plant species identification
#     return "plant species" in response.lower()