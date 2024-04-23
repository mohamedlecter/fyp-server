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

# Helper function to fetch all plants
def get_plants():
    response = app.test_client().get('/plant/')
    return response

def test_get_plants(client):
    # Test fetching all plants
    logging.info("Testing fetching all plants")
    response = get_plants()
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 200")
    assert response.status_code == 200

# Helper function to fetch plant by ID
def get_plant_by_id(plant_id):
    response = app.test_client().get(f'/plant/{plant_id}')
    return response

def test_get_plant_by_id(client):
    # Test fetching plant by ID with a non-existing ID
    logging.info("Testing fetching plant by ID with a non-existing ID")
    plant_id = '609a62fcbf61f33d48a4eb23'  # Non-existing plant ID
    response = get_plant_by_id(plant_id)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 404")
    assert response.status_code == 404

# Helper function to search plants by name
def search_plants(plant_name):
    response = app.test_client().get(f'/plant/search/{plant_name}')
    return response

def test_search_plants(client):
    # Test searching plants by name
    logging.info("Testing searching plants by name")
    plant_name = 'Apple'
    response = search_plants(plant_name)
    logging.info("Response status code: %s", response.status_code)
    logging.info("Expected status code: 200")
    assert response.status_code == 200


