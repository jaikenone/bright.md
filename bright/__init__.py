import logging

from logging.handlers import RotatingFileHandler
from flask import Flask

from .models import db
from . import config


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()

    flask_app.logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(f"./{__name__}.log", maxBytes=1000000, backupCount=5)
    handler.setFormatter(formatter)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(handler)
    flask_app.logger.setLevel(logging.DEBUG)
    flask_app.logger.addHandler(handler)

    flask_app.logger.info("Start serving...")

    return flask_app