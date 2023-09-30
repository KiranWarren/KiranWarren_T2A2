from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

def init_app():

    app = Flask(__name__)

    # Configuration
    app.config.from_object("config.app_config")
    jwt = JWTManager(app)

    # Connect DB via ORM
    db.init_app(app)

    # Connect Schemas
    ma.init_app(app)

    # CLI Commands
    from commands import db_commands
    app.register_blueprint(db_commands)

    # Connect Routes & Controllers
    from controllers import register_controllers
    for controller in register_controllers:
        app.register_blueprint(controller)

    return app