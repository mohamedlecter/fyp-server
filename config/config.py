from pymongo import MongoClient
from flask_bcrypt import Bcrypt

class Config:
    MONGODB_CONNECTION_STRING = 'mongodb+srv://admin:admin@cluster0.xkuprjf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client.get_database('final-year-project')
    bcrypt = Bcrypt()