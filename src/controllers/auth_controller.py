from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_bcrypt import Bcrypt

from main import db
from models.users import User
from schemas.user_schema import user_schema, login_schema

bcrypt = Bcrypt()
auths = Blueprint('auth', __name__, url_prefix="/auth")

# Error handlers
@auths.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@auths.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@auths.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"error": f"The field `{e}` is required."}), 400

@auths.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400

@auths.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Register a New User
# /auth/register
@auths.route("/register", methods=["POST"])
def register_user():
    '''
    
    '''
    user_json = user_schema.load(request.json)
    new_user = User()

    # Map json to new user
    new_user.username = user_json["username"]
    new_user.email_address = user_json["email_address"]
    new_user.position = user_json.get("position")
    new_user.location_id = user_json["location_id"]

    # Hash password before storing
    new_user.password = bcrypt.generate_password_hash(user_json["password"]).decode("utf-8")

    # Add to the database and commit changes
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {new_user.username} has been registered successfully."})


# Login User
# /auth/login
@auths.route("/login", methods=["POST"])
def login_user():
    login_json = login_schema.load(request.json)
    query = db.select(User).filter_by(username=request.json["username"])
    user = db.session.scalar(query)

    if not user or not bcrypt.check_password_hash(user.password, login_json["password"]):
        return jsonify({"error": "The username or password you have entered is incorrect. Please try again."})

    return jsonify({"great": "success"})


