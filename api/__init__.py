from flask import Flask
from flask_cors import CORS

from .routes import tasks_api
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("api.config.BaseConfig")

    CORS(app)


    tasks_api.init_app(app)
    db.init_app(app)

    return app
