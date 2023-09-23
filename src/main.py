from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

'''
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
'''


def init_app():

    app = Flask(__name__)

    # Configuration
    app.config.from_object("config.app_config")


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