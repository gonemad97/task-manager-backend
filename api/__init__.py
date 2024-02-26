from flask import Flask
from flask_cors import CORS

from .routes import tasks_api
from .models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object("api.config.BaseConfig")

    CORS(app)

    tasks_api.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        user1 = User(username="jack")
        user1.set_password("apple")
        user1.save()

        user2 = User(username="jill")
        user2.set_password("orange")
        user2.save()
    return app
