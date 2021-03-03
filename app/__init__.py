from flask import Flask


application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")

from app import views
from app import Models
from app import application

