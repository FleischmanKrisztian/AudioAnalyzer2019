import pymongo
from app import application
from flask_pymongo import PyMongo
import pyAudioAnalysis , ffmpeg, pymongo, pydub, os, uuid, io, datetime

class Config(object):
    DEBUG= False
    TESTING = False

    SECRET_KEY = b'\x0b\xc8\xe1\xd9\xf7\xf6\xa9\xd9\xba\xd3\xfb\xa0\x16\x87\x80\xe4'
    DB_NAME = "production-db"
    
    #DEFAULT VARIABLES
    MAX_AUDIO_FILESIZE = 300000000
    CLIENT_FILES = "../app/static/client/audiofiles/"
    UPLOAD_FOLDER = "../Flasklast/audiofiles/"
    SPEC_FOLDER = "../Flasklast/app/static/dynamicimg/"
    MEL_FOLDER = "../Flasklast/app/static/dynamicimg/"
    CHANNEL_FOLDER = "../Flasklast/app/static/client/audiofiles/"
    TEMPO_FOLDER = "../Flasklast/app/static/dynamicimg/"
    QUALITY_FOLDER = "../Flasklast/app/static/dynamicimg/"
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