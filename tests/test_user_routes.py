import json
import uuid
import pytest
import logging
from app import app

# Enable logging
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Helper function to register a user
def register_user(data):
    response = app.test_client().post('/user/signup', json=data)
    return response

# Helper function to login a user
def login_user(data):
    response = app.test_client().post('/user/login', json=data)
    return response

def test_register_user(client):
    # Test registration with valid data
    logging.info("Testing registration with valid data")
    data = {'username': 'testuser', 'password': 'passwordtesting', 'email': 'newUserEmail12345677@example.com'}
    response = register_user(data)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 201")
    assert response.status_code == 201

    # Test registration with missing fields
    logging.info("Testing registration with missing fields")
    data = {'username': 'testuser', 'email': 'newUserEmail12345677@8example.com'}
    response = register_user(data)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 400")
    assert response.status_code == 400

def test_login_user(client):
    # Test login with correct credentials
    logging.info("Testing login with correct credentials")
    data = {'email': 'newUserEmail12345677@example.com', 'password': 'passwordtesting'}
    response = login_user(data)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 200")
    assert response.status_code == 200

    # Test login with incorrect password
    logging.info("Testing login with incorrect password")
    data = {'email': 'newUserEmail12345677@example.com', 'password': 'wrongpassword'}
    response = login_user(data)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 401")
    assert response.status_code == 401

def test_get_all_users(client):
    # Test fetching all users
    logging.info("Testing fetching all users")
    response = client.get('/user/')
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 200")
    assert response.status_code == 200
    
def test_register_user_email_exists(client):
    # Test registration with existing email
    logging.info("Testing registration with existing email")
    # Create an existing user with a specific email
    existing_user = {'username': 'existing_user', 'password': 'password123', 'email': 'existing@example.com'}
    register_user(existing_user)

    # Attempt to register with the same email
    data = {'username': 'existing_user', 'password': 'newpassword456', 'email': 'existing@example.com'}
    response = register_user(data)

    # Check that the server responds with a 400 status code
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 400")
    assert response.status_code == 400

    # Check that the response contains an error message indicating that the email already exists
    expected_error_message = {'error': 'Email already exists'}
    logging.info("Response data: %s", response.json)
    logging.info("Expected data: %s", expected_error_message)
    assert response.json == expected_error_message

def test_get_user_by_id(client):
    # Test fetching user by ID (replace 'user_id' with an actual user ID)
    logging.info("Testing fetching user by ID")
    response = client.get('/user/655c6c7c8cc648949c86a5e8')
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 200")
    assert response.status_code == 200