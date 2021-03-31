import pymongo
import os
from app import application
from flask_pymongo import PyMongo

class Config(object):
    DEBUG= False
    TESTING = False

    DB_NAME = "production-db"
    
    MAX_AUDIO_FILESIZE = 30000000
    SECRET_KEY = os.environ["SECRET_KEY"]
    SPOTIFY_ID = os.environ["SPOTIFY_ID"]
    SPOTIFY_SECRET = os.environ["SPOTIFY_SECRET"]
    MONGO_URI = os.environ["SOUNRAVEL_MONGO_URI"]

    TESTING_PATH = "./app/static/client/IncomingAudio/"
    UPLOAD_FOLDER = "./app/static/client/IncomingAudio/"
    CLIENT_AUDIOFILES = "./app/static/client/audiofiles/"
    CLIENT_IMAGES = "./app/static/client/images/"
    CLIENT_AUDIO = "./app/static/client/audiofiles/"
    CLIENT_FOLDER = "./app/static/client/audiofiles/"

    #DATABASE
    application.config['MONGO_URI'] = MONGO_URI
    mongo = PyMongo(application)


class ProductionConfig(Config):
    DEBUG=False
    TESTING = False

    TESTING_PATH = "./app/static/client/IncomingAudio/"
    UPLOAD_FOLDER = "./app/static/client/IncomingAudio/"
    CLIENT_AUDIOFILES = "./app/static/client/audiofiles/"
    CLIENT_IMAGES = "./app/static/client/images/"
    CLIENT_AUDIO = "../app/static/client/audiofiles/"
    CLIENT_FOLDER = "./app/static/client"

    client = pymongo.MongoClient(application.config['MONGO_URI'])

class DevelopmentConfig(Config):
    DEBUG= True
    TESTING = False

    TESTING_PATH = "./app/static/client/IncomingAudio/"
    UPLOAD_FOLDER = "./app/static/client/IncomingAudio/"
    CLIENT_AUDIOFILES = "./app/static/client/audiofiles/"
    CLIENT_IMAGES = "./app/static/client/images/"
    CLIENT_AUDIO = "./static/client/audiofiles/"
    CLIENT_FOLDER = "./app/static/client"

    client = pymongo.MongoClient(application.config['MONGO_URI'])

class TestingConfig(Config):
    TESTING = True