from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import db, bcrypt
from models.users import User
from models.comments import Comment
from schemas.user_schema import user_schema, users_schema
from schemas.comment_schema import comments_schema
from controllers.auths_controller import check_admin

users = Blueprint('user', __name__, url_prefix="/users")

# Error handlers
@users.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@users.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@users.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@users.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@users.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# UPDATE User Information
# /users/update_info
@users.route("/update_info/", methods=["PATCH"])
@jwt_required()
def update_user_information():
    '''
    This route will be used by a user to update their own information. Their identity provided by the jwt token will
    be used to query the database. This will ensure that a user can only change their own information.

    This function will not change the following fields:
    - The `is_admin` field is not modified by this function, and is instead changed by the promote_user_to_admin function 
        in auths_controller.py. Admin level authorisation is required for that.
    - The `username` field cannot be changed. Users must keep the username they are assigned as it will be based on their name.

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The following database query will filter the users.username column to match the username given from the jwt identity.
    Database statement: SELECT * FROM users WHERE username=get_jwt_identity();

    Example json body for PATCH request:
    {
        "email_address": "OPTIONAL, valid email address",
        "position": "OPTIONAL, string",
        "password": "OPTIONAL, string between 6 and 25 chars",
        "location_id": "OPTIONAL, integer"
    }

    JWT is required for this route.
    '''
    # Get the identity of the user using this route.
    username = get_jwt_identity()
    query = db.select(User).filter_by(username=username)
    user = db.session.scalar(query)
    response = user_schema.dump(user)
    
    # Validate input coming from json request using schema.
    # Load-only fields need dummy data if not passed by the user.
    if request.json.get("email_address"):
        response["email_address"] = request.json["email_address"]
    if request.json.get("location_id"):
        response["location_id"] = request.json["location_id"]
    else:
        response["location_id"] = 1
    if request.json.get("position"):
        response["position"] = request.json["position"]
    if request.json.get("password"):
        response["password"] = request.json["password"]
    else:
        response["password"] = "password"
    response = user_schema.load(response)

    # Map the json request properties to the user if they are given.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("email_address"):
        user.email_address = request.json["email_address"]
        changed_string = " email_address"
    if request.json.get("location_id"):
        user.location_id = request.json["location_id"]
        changed_string += " location_id"
    if request.json.get("position"):
        user.position = request.json["position"]
        changed_string += " position"
    if request.json.get("password"):
        user.password = bcrypt.generate_password_hash(request.json["password"]).decode("utf-8")
        changed_string += " password"

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No user information has been changed.")

    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following user information has been changed:{changed_string}.", **user_schema.dump(user))


# GET all Users
# /users/
@users.route("/", methods=["GET"])
@jwt_required()
def get_users_list():
    '''
    This route will be used to see all users of the application, therefore a GET request is used.

    The following database query will return all entries in the users table. The hashed password is load_only and not displayed.
    Database statement: SELECT * FROM users;

    JWT is required for this route.
    '''
    query = db.select(User)
    user_list = db.session.scalars(query)
    response = users_schema.dump(user_list)

    return jsonify(response)


# GET a User by User ID
# /users/<id>
@users.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id: int):
    '''
    This route is used to find a specific user based on the user id provided in the URL. The user id passed in the URL
    must be an integer and must exist in the users table.

    The following data query will return the user with the matching user id passed in the URL. The hashed password is 
    load_only and not displayed.
    Database statement: SELECT * FROM users WHERE id=user_id;

    JWT is required for this route.
    '''
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    response = user_schema.dump(user)

    if not response:
        return jsonify(error=f"A user with id=`{user_id}` does not exist in the database."), 404

    return jsonify(response)


# DELETE a User by User ID
# /users/delete_user/<id>
@users.route("/delete_user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_by_id(user_id: int):
    '''
    This route is used by an admin to remove a user from the users table. The user to be removed will have a matching id to
    the user_id passed in the URL. The user id passed in the URL must be an integer and must exist in the users table.

    The "/delete_user/" portion of the URL was added to make sure that this action was deliberate and less prone to mistake.
    Accidentally deleting a user would have flow on effects to comments due to the cascade delete.

    The following data query will return the user with the matching user id passed in the URL.
    Database statement: SELECT * FROM users WHERE id=user_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Filter the user with the matching user_id.
    user = User.query.filter_by(id=user_id).first()
    response = user_schema.dump(user)

    # Provide response if that user_id does not exist.
    if not response:
        return jsonify(error=f"A user with `id`={user_id} does not exist in the database. No deletions have been made."), 404

    # Delete user and provide feedback of successful deletion.
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "message": f"The user with id=`{user_id}` has been deleted successfully."
    })


# GET all Comments by User ID
# /users/<id>/comments
@users.route("/<int:user_id>/comments", methods=["GET"])
@jwt_required()
def get_comments_by_user(user_id: int):
    '''
    This route will be used to see all comments made by a specific user. The user is filtered by providing a user ID in the 
    URL.

    The following database query will return the unique entry in the users table with matching id provded by the URL.
    Database statement: SELECT * FROM users WHERE id=user_id;

    The following database query will return all entries in the comments table with matching user_id.
    Database query: SELECT * FROM comments WHERE user_id=user_id;

    JWT is required for this route.
    '''
    # First ensure that a user with the provided user_id exists in the database.
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    response = user_schema.dump(user)

    # Provide feedback that the user they're looking for does not exist in the database.
    if not response:
        return jsonify(error=f"A user with id=`{user_id}` does not exist in the database."), 404

    # Query the database to find all comments made by the user with id=user_id.
    query = db.select(Comment).filter_by(user_id=user_id)
    comments_list = db.session.scalars(query)
    response = comments_schema.dump(comments_list)

    # If the user has not made any comments, provide this feedback to the user so they know it's actually working.
    if not response:
        return jsonify(message=f"The user with id=`{user_id}` has not posted any comments."), 200

    # Return all comments made by the user.
    return jsonify(response)