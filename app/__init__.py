from flask import Flask
import os

application = Flask(__name__)
application.config.from_object("config.ProductionConfig")
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(port=port)

from app import views
from app import Models
from app import application