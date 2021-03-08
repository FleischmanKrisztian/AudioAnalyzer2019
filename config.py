import pymongo
import os
from app import application
from flask_pymongo import PyMongo

class Config(object):
    DEBUG= False
    TESTING = False

    SECRET_KEY = os.environ["SECRET_KEY"]
    DB_NAME = "production-db"
    
    #DEFAULT VARIABLES
    MAX_AUDIO_FILESIZE = 300000000
    SPOTIFY_ID = os.environ["SPOTIFY_ID"]
    SPOTIFY_SECRET = os.environ["SPOTIFY_SECRET"]
    UPLOAD_FOLDER = "../Flasklast/app/static/client/IncomingAudio/"
    CLIENT_FILES = "../Flasklast/app/static/client/"
    CLIENT_AUDIOFILES = "../Flasklast/app/static/client/audiofiles/"
    CLIENT_IMAGES = "../Flasklast/app/static/client/images/"
    CLIENT_AUDIO = "../app/static/client/audiofiles/"
    MONGO_URI = os.environ["SOUNRAVEL_MONGO_URI"]
  
    #DATABASE
    application.config['MONGO_URI'] = MONGO_URI
    mongo = PyMongo(application)


class ProductionConfig(Config):
    DEBUG=False
    TESTING = False

    client = pymongo.MongoClient(application.config['MONGO_URI'])

class DevelopmentConfig(Config):
    DEBUG= False
    TESTING = False

    client = pymongo.MongoClient(application.config['MONGO_URI'])

class TestingConfig(Config):
    TESTING = True