from flask import Flask
from flask_cors import CORS

application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")
CORS(application, resources={r'/*': {'origins': '*'}})

from app import views
from app import admin_views
from app import Models
from app import application