from flask import Flask
import os

application = Flask(__name__)
application.config.from_object("config.ProductionConfig")
# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))
# application.run(host='127.0.0.1', port=port)

from app import views
from app import Models
from app import application

