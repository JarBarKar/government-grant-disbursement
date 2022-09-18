import os
from flask import Flask
from .extensions import db
from flask_cors import CORS
from .routes.grant import grant
from .routes.member import member
from .routes.household import household


def create_app():
    """Initialize Flask app with the DB config and blueprints

    Returns:
        app : Initalized Flask app 
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ.get("DB_ACCOUNT_ID")}:{os.environ.get("DB_ACCOUNT_PASSWORD")}@127.0.0.1:3306/government-grant-disbursement'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(member)
    app.register_blueprint(household)
    app.register_blueprint(grant)

    CORS(app)

    return app
