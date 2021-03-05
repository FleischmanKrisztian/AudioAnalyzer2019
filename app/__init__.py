from flask import Flask

application = Flask(__name__)
application.config.from_object("config.ProductionConfig")
application.run(host= '0.0.0.0', port=5000)

from app import views
from app import Models
from app import application

