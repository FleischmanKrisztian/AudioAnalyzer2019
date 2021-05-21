from app import application
from app.Modules import spotifyapi, DatabaseActions
from app.Models import User, Audiofile
from flask import session, send_from_directory, abort, render_template, request, redirect, make_response
from functools import wraps

import json

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
        code = DatabaseActions.add_to_db(user)
        if code[1] == 200:
            return render_template("public/index.html")
        else:
            return render_template("public/sign_up.html")

    return render_template("public/sign_up.html")

# import shutil
@application.route("/about")
def about():
    # shutil.rmtree(path=application.config["CLIENT_FOLDER"])
    return render_template("public/about.html")

@application.route("/profile")
@login_required
def profile():
    emailFromCookie = request.cookies.get('email')
    userAsJson = DatabaseActions.getuser(emailFromCookie)
    json_string = json.dumps(userAsJson) 
    name = DatabaseActions.attributeFromJson(json_string , "name")
    email = DatabaseActions.attributeFromJson(json_string , "email")
    creationDate = DatabaseActions.attributeFromJson(json_string , "creationDate")
    lastLogin = DatabaseActions.attributeFromJson(json_string , "lastLogin")
    scannedFiles = DatabaseActions.attributeFromJson(json_string , "scannedFiles")

    return render_template("public/profile.html", name=name, email = email, creationDate = creationDate, lastLogin = lastLogin, scannedFiles = scannedFiles)

@application.route("/results")
def results(audioname="nofileprovided"):
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
        code = DatabaseActions.login()
        if code[1] == 200:
            return render_template("public/index.html")
        else:
            return render_template("public/login.html")
    
    return render_template("public/login.html")

@application.route("/getfile/<path:filename>")
def getfile(filename):
    try:
        return send_from_directory(application.config['CLIENT_AUDIO'],filename,as_attachment=True)
    except FileNotFoundError:
        abort(404)

@application.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if 'audiofile' in request.files:
            if not allowed_audio_filesize(request.cookies.get("filesize")):
                print("File exceeded maximum size")
                return render_template("public/upload.html")
            else:
                DatabaseActions.incrementFilesUploaded(request.cookies.get('email'))
                audiofile = Audiofile.Audiofile()
                audiofile.SaveToFolder()
                audiofile.ConvertAudiofile()
                id = spotifyapi.Get_id_of_song(audiofile.name)
                if Filefound(id):
                    tempo = (spotifyapi.tempo_of_id(id[0]))
                    key = (spotifyapi.key_of_id(id[0]))
                    tempo = tempo[0]
                    key = key[0]
                    existsonspotify = True
                else:
                    tempo = "No song was found on spotify"
                    key = "No song was found on spotify"
                    existsonspotify = False
                
                audiofile.GenerateData()

                    
        return render_template("public/results.html",nameofsong=audiofile.name, numberofchannels = audiofile.numberofchannels, keyofsong=key, tempoofsong=tempo, idofsong = id[0], existsonspotify = existsonspotify)  
    return render_template("public/upload.html")

    

    