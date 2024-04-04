import os
from openai import OpenAI


# Initialize OpenAI client with API key
client = OpenAI(
    api_key="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",
)

# Initialize evaluation metrics
total_responses = 0
relevant_responses = 0
accurate_completions = 0
total_interactions = 0
errors = 0
successful_task_completions = 0
total_tasks = 0

def chatbot(user_message):
    global total_responses, relevant_responses, accurate_completions, total_interactions, errors, successful_task_completions, total_tasks

    # Increment total interactions
    total_interactions += 1

    # Define the conversation messages focusing on plant-related queries
    messages = [
        {"role": "system", "content": "Welcome to the Plant Assistant Bot! I'm here to help you with plant-related queries."},
        {"role": "user", "content": user_message}
    ]

    # Generate a completion using the chat model
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages
    )

    # Extract bot's response
    bot_reply = completion.choices[0].message.content

    # Increment total responses
    total_responses += 1

    # Evaluate response relevance
    if is_response_relevant(bot_reply):
        relevant_responses += 1

    # Evaluate completion accuracy
    if is_completion_accurate(completion):
        accurate_completions += 1

    # Evaluate error rate
    if is_error_present(bot_reply):
        errors += 1

    # Update task completion metrics (if applicable)
    # For demonstration purposes, let's assume a specific task: "Identifying plant species"
    total_tasks += 1
    if is_task_completed(bot_reply):
        successful_task_completions += 1

    return bot_reply

def is_response_relevant(response):
    # Implement logic to determine relevance of response
    # For simplicity, let's assume all responses are relevant
    return True

def is_completion_accurate(completion):
    # Implement logic to determine accuracy of completion
    # For simplicity, let's assume all completions are accurate
    return True

def is_error_present(response):
    # Implement logic to determine if error is present in response
    # For simplicity, let's assume there are no errors
    return False

def is_task_completed(response):
    # Implement logic to determine if a specific task is completed based on response
    # For demonstration purposes, let's assume the task is completed if the bot provides a plant species identification
    return "plant species" in response.lower()