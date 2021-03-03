import pymongo
from datetime import date
from flask import request, session
from passlib.hash import pbkdf2_sha256
import json
from app import application

client = pymongo.MongoClient(application.config["MONGO_URI"])
db = client.Users

def getuser(email):
    userAsJson = db.users.find_one({'email':email})
    return userAsJson

def attributeFromJson(jsonstring,field):
    resp_dict = json.loads(str(jsonstring))
    return resp_dict.get(field)

def add_to_db(user):
    if db.users.find_one({"email":user.email}):
        return ("This E-mail is already in use!"), 403
    else:
        jsonstring = user.usertojson()
        db.users.insert_one(jsonstring)
        return start_session(jsonstring), 200
    return ("There was an error while adding to Database!"), 500

def loginFunction():
    email = request.form.get('email')
    user = db.users.find_one({ "email": email })
    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
        if request.form.get('rememberme') == "on":
            user['rememberme'] = True
        else:
            user['rememberme'] = False
        user['lastLogin'] = str(date.today())
        update_user(user, email)
        return start_session(user), 200

    return ("Invalid Login Credentials!"), 401

def update_user(user, email):
    try:
        db.users.delete_one({"email":email})
        db.users.insert_one(user)
        return ("Updated successfully"), 200
    except:
        return ("there was an error with updating"), 500

def start_session(user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return (user), 200

def incrementFilesUploaded(email):
    userAsJson = db.users.find_one({'email':email})
    scannedFiles = int(userAsJson['scannedFiles'])
    scannedFiles = scannedFiles + 1
    userAsJson['scannedFiles'] = scannedFiles
    update_user(userAsJson, email)
    return userAsJson

