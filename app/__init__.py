from flask import Flask

application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")
# application.secret_key = b'\x0b\xc8\xe1\xd9\xf7\xf6\xa9\xd9\xba\xd3\xfb\xa0\x16\x87\x80\xe4'     
from app import views
from app import admin_views
from app import Models
from app import application