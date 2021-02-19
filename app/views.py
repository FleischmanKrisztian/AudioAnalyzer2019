from app import application
from app import spotifyapi
from flask import session, redirect
from functools import wraps
from .Models.user import User
from.Models.Functions import getuser, attributeFromJson, incrementFilesUploaded, add_to_db, loginFunction
from .Models.audiofile import Audiofile
from flask import render_template, request, redirect, jsonify
from flask import make_response
import json
import threading, concurrent.futures

#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/login')
    return wrap

def Filefound(f):
        if f[1] == 200:
            return True
        else:
            return False

def allowed_audio_filesize(filesize):

    if int(filesize) <= application.config["MAX_AUDIO_FILESIZE"]:
        return True
    else:
        return False

@application.route("/")
def index():
      
    return render_template("public/index.html")

@application.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        user = User()
        code = add_to_db(user)
        if code[1] == 200:
            return render_template("public/index.html")
        else:
            return render_template("public/sign_up.html")

    return render_template("public/sign_up.html")

@application.route("/about")
def about():
    return render_template("public/about.html")

@application.route("/profile")
@login_required
def profile():
    emailFromCookie = request.cookies.get('email')
    userAsJson = getuser(emailFromCookie)
    json_string = json.dumps(userAsJson) 
    name = attributeFromJson(json_string , "name")
    email = attributeFromJson(json_string , "email")
    creationDate = attributeFromJson(json_string , "creationDate")
    lastLogin = attributeFromJson(json_string , "lastLogin")
    scannedFiles = attributeFromJson(json_string , "scannedFiles")

    return render_template("public/profile.html", name=name, email = email, creationDate = creationDate, lastLogin = lastLogin, scannedFiles = scannedFiles)

@application.route("/results")
def results(audioname="nofileprovided"):
    print(audioname)
    return render_template("public/results.html", nameofsong = audioname)

@application.route("/signout")
@login_required
def signout():
    resp = make_response(render_template('public/index.html'))
    resp.set_cookie('email', expires=0)
    session.clear()
    return resp

@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        code = loginFunction()
        if code[1] == 200:
            return render_template("public/index.html")
        else:
            return render_template("public/login.html")
    
    return render_template("public/login.html")

@application.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if 'audiofile' in request.files:
            if not allowed_audio_filesize(request.cookies.get("filesize")):
                print("File exceeded maximum size")
                return render_template("public/upload.html")
            else:
                audiofile = Audiofile()
                audiofile.convert_audiofile()
                # id = spotifyapi.idOfSong(audiofile.name)
                # if Filefound(id):
                #     tempo = (spotifyapi.tempo_of_id(id[0]))
                #     key = (spotifyapi.key_of_id(id[0]))
                #     audiofile.tempo = tempo[0]
                #     audiofile.key = key[0]
                #     print (str(audiofile.key) + " " + str(audiofile.tempo))
                # t1 = threading.Thread(target=audiofile.spectrogram_audiofile)
                # t1.start()
                # t2 = threading.Thread(target=audiofile.separate_audiofile,args=[2])
                # t2.start()
                # t3 = threading.Thread(target=audiofile.channel_audiofile)
                # t3.start()
                # t1.join()
                # t4 = threading.Thread(target=audiofile.librosa_spectrogram)
                # t4.start()
                # t4.join()
                # t5 = threading.Thread(target=audiofile.tempo_graph)
                # t5.start()
                # t5.join()    
                # t6 = threading.Thread(target=audiofile.quality_spectrogram)
                # t6.start()
                emailFromCookie = request.cookies.get('email')
                t7 = threading.Thread(target=incrementFilesUploaded,args=[emailFromCookie])
                t7.start()
                # t6.join()
                # t3.join()
                # t2.join()
                    
        return render_template("public/results.html",nameofsong=audiofile.name)  
    return render_template("public/upload.html")

    

    