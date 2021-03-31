from flask import Flask
import os

application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(port=port)

from app.Modules import views
from app import Models
from app import application

