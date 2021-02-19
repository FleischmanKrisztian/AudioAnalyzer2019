from datetime import date
from passlib.hash import pbkdf2_sha256
from flask import jsonify, session, redirect, request
import uuid
import pymongo
from app import application

#DATABASE
client = pymongo.MongoClient(application.config["MONGO_URI"])
db = client.Users

class User:
    #create a user with info from signup and ecrypting the password field
    def __init__(self):
        id = uuid.uuid4().hex
        self._id = id
        self.name = request.form.get('name')
        self.email = request.form.get('email')
        self.password = pbkdf2_sha256.encrypt(request.form.get('password'))
        self.creationDate = str(date.today())
        self.lastlogin = str(date.today())
        self.rememberme = request.form.get('rememberme')
        self.scannedFiles = 0
        
    def usertojson(self):
        user = {
            "_id":self._id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "rememberme":self.rememberme,
            "lastLogin":self.lastlogin,
            "creationDate":self.creationDate,
            "scannedFiles":self.scannedFiles
        }
        return user


     