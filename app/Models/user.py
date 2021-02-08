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
        self.scannedFiles = 0
        
    def Usertojson(self):
        user = {
            "_id":self._id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "creationDate":self.creationDate,
            "scannedFiles":self.scannedFiles
        }
        return user

    def display_user(self):
        return ("The users id is " + self._id + " name is: " + self.name + " password " + self.password)  

    def add_to_db(self):
        if db.users.find_one({"email":self.email}):
            return jsonify({"error": "Email address already in use"}), 400
        else:
            jsonstring = self.Usertojson()
            if db.users.insert_one(jsonstring):
                return self.start_session(jsonstring), 200
        return jsonify({"error": "Signup failed!"}), 400

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user), 200
        
        return jsonify({ "error": "Invalid Login Credentials"}), 401


        

     