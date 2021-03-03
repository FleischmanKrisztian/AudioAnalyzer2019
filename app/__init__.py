from flask import Flask
from app import views
from app import Models
from app import application

application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")

