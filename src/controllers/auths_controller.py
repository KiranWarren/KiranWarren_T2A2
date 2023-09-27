from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, login_schema

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
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@auths.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@auths.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


def check_admin():
    '''
    This helper function is used throughout the application to check for is_admin=True before allowing use of admin-level
    access routes.

    The following database query will filter the users.username column to match the username given from the JWT identity.
    Database statement: SELECT * FROM users WHERE username=get_jwt_identity();

    For the matching user entry in the users table, the is_admin attribute will be returned (True/False).
    '''
    # Get the identity of the user using this route & check is_admin=True.
    username = get_jwt_identity()
    query = db.select(User).filter_by(username=username)
    user = db.session.scalar(query)
    return user.is_admin


# Register a New User
# /auth/register
@auths.route("/register", methods=["POST"])
def register_user():
    '''
    This route will create a new user with the information provided in the json request. After registration of the user,
    this user will be logged into the application (JWT returned).

    This route involves creation of a new resource in the data table, and therefore the POST method is most appropriate.

    The following database statement is used to add the entry into the users table.
    Database statement: INSERT INTO users (username, email_address, position, location_id, is_admin, password)
    VALUES (user_json["username"], user_json["email_address"], user_json["position"], user_json["location_id"], 
    False, bcrypt.generate_password_hash(user_json["password"]).decode("utf-8"));

    Example json body for POST request:
    {
        "username": "string between 2 and 25 chars",
        "email_address": "valid email address",
        "position": "OPTIONAL, string",
        "password": "string between 6 and 25 chars",
        "location_id": "integer"
    }

    No authentication or authorisation is required for this route. Ideally, there would be some verification that the user
    registering for this route is an employee at the company, however, this falls out of the scope of this assignment.
    '''
    user_json = user_schema.load(request.json)
    new_user = User()

    # Map json to new user
    new_user.username = user_json["username"]
    new_user.email_address = user_json["email_address"]
    new_user.position = user_json.get("position")
    new_user.location_id = user_json["location_id"]
    new_user.is_admin = False

    # Hash password before storing
    new_user.password = bcrypt.generate_password_hash(user_json["password"]).decode("utf-8")

    # Add to the database and commit changes
    db.session.add(new_user)
    db.session.commit()

    # Create an access token that expires in 1 day
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=user_json["username"], expires_delta=expiry)

    return jsonify(message=f"User {new_user.username} has been registered successfully.", user=user_json["username"], access_token=access_token)


# Login User
# /auth/login
@auths.route("/login", methods=["POST"])
def login_user():
    '''
    This route allows users to log into the API webserver application. The username and password they supply must match
    the username and password of an entry within the users table. Upon successful match, they will be logged into the application
    as the matched user. A JWT will be provided to the user, which they can add as a bearer token to any further requests made
    to the API webserver.

    The following database query will return the user with the matching username passed in the json request.
    Database statement: SELECT * FROM users WHERE username=request.json["username"];

    Example json body for POST request:
    {
        "username": "string between 2 and 25 chars",
        "password": "string between 6 and 25 chars"
    }

    This route performs authentication, so no prior authentication is required for this route.
    '''
    login_json = login_schema.load(request.json)
    query = db.select(User).filter_by(username=login_json["username"])
    user = db.session.scalar(query)

    # Check if user exists and that the entered password matches
    if not user or not bcrypt.check_password_hash(user.password, login_json["password"]):
        return jsonify({"error": "The username or password you have entered is incorrect. Please try again."}), 401
    
    # Create an access token that expires in 1 day
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=login_json["username"], expires_delta=expiry)

    return jsonify(message=f"Login successful. Welcome back, {login_json['username']}.", user=login_json["username"], access_token=access_token)


# Promote User to Admin-Level Authorisation
# /auth/promote_to_admin/
@auths.route("/promote_to_admin/", methods=["PATCH"])
@jwt_required()
def promote_user_to_admin():
    '''
    This route will be used by an admin to increase the level of authorisation to admin level for another user. If the
    user already has admin-level access, no changes will be made and response detailling this will be returned. The user's
    username will be sent via json body in the request. This design choice was made because it feels more deliberate and
    less prone to error than sending a users.id via URL.

    A PATCH request seems most appropriate here, as only one field is being updated for the user entry.

    The following database query will filter the users.username column to match the username given from the request json.
    Database statement: SELECT * FROM users WHERE username='request.json["username"]';

    Example json body for PATCH request:
    {
        "username": "string between 2 and 25 chars"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Extract username from json request and filter users.username
    username=request.json["username"]
    query = db.select(User).filter_by(username=username)
    user = db.session.scalar(query)
    response = user_schema.dump(user)

    # First check that a user exists with the given username.
    if response:
        # Check if they already have admin authorisation
        if user.is_admin == True:
            return jsonify(message=f"User `{username}` already has admin level access.")
        else:
            # Set user authorisation to admin level
            user.is_admin = True

            # Commit changes
            db.session.commit()
            return jsonify(message=f"Authorisation level has been increased for user `{username}`.", **user_schema.dump(user))

    return jsonify({"error": f"A user with `username`={username} does not exist in the database. No updates have been made."}), 404
