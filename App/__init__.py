import os
from flask import Flask
from .extensions import db
from flask_cors import CORS
from .routes.grant import grant
from .routes.member import member
from .routes.household import household


def create_app(config_file='settings.py'):
    """Initialize Flask app with the DB config and blueprints

    Returns:
        app : Initalized Flask app 
    """
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(member)
    app.register_blueprint(household)
    app.register_blueprint(grant)

    CORS(app)

    return app
