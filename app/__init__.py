from .config import Config
from .extensions import db
from .views import main_blueprint
from flask import Flask, Blueprint
import time


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_blueprint)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
