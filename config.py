import pymongo
from app import application
from flask_pymongo import PyMongo

class Config(object):
    DEBUG= False
    TESTING = False

    SECRET_KEY = b'\x0b\xc8\xe1\xd9\xf7\xf6\xa9\xd9\xba\xd3\xfb\xa0\x16\x87\x80\xe4'
    DB_NAME = "production-db"
    
    #DEFAULT VARIABLES
    MAX_AUDIO_FILESIZE = 300000000
    UPLOAD_FOLDER = "../Flasklast/app/static/client/IncomingAudio/"
    CLIENT_FILES = "../Flasklast/app/static/client/"
    CLIENT_IMAGES = "../Flasklast/app/static/client/images/"
    CLIENT_AUDIO = "../app/static/client/audiofiles/"
    MONGO_URI = "mongodb+srv://Krisztian:Password1@flaskappcluster.5akml.mongodb.net/<dbname>?retryWrites=true&w=majority"

    
#DATABASE
application.config['MONGO_URI'] = "mongodb+srv://Krisztian:Password1@flaskappcluster.5akml.mongodb.net/Audiofiles?retryWrites=true&w=majority"
mongo = PyMongo(application)


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG= True
    TESTING = False

    SECRET_KEY = b'\x0b\xc8\xe1\xd9\xf7\xf6\xa9\xd9\xba\xd3\xfb\xa0\x16\x87\x80\xe4'
    DB_NAME = "production-db"
    #DATABASE
    client = pymongo.MongoClient("mongodb+srv://Krisztian:Password1@flaskappcluster.5akml.mongodb.net/<dbname>?retryWrites=true&w=majority")
    #DEFAULT VARIABLES
    MAX_AUDIO_FILESIZE = 300000000

class TestingConfig(Config):
    TESTING = True