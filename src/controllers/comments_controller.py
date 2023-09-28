from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

from main import db
from models.comments import Comment
from models.users import User
from schemas.comment_schema import comment_schema, comments_schema

comments = Blueprint('comment', __name__, url_prefix="/comments")

# Error handlers
@comments.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@comments.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@comments.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@comments.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@comments.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a comment
# /comments/
@comments.route("/", methods=["POST"])
@jwt_required()
def post_comment():
    '''
    This route is used by users to post a comment about a project. Users can make multiple comments on the same project.
    The when_created attribute will be automated assigned using datetime.now(). The lasts_edited date will be left
    empty. The user_id field will be automatically populating by using the get_jwt_identity() to query the database to find
    the current user's user_id. This means that the user will only have to include the comment and project_id in their
    request.

    The following statement will be used to find the current user's user_id by way of get_jwt_identity().
    Database statement: SELECT * FROM users WHERE username=get_jwt_identity();

    The following statement will be used to create the entry in the comments data table.
    Database statement: INSERT INTO comments (comment, when_created, last_edited, project_id, user_id) 
    VALUES (request.json["comment"], datetime.datetime.now(), None, request.json["project_id"], user.id);

    Example json body for POST request:
    {
        "comment": "string",
        "project_id": "integer"
    }

    JWT is required for this route.
    '''
    # Load the request json into the comment schema.
    comment_json = comment_schema.load(request.json)

    # Add the date attributes
    comment_json["when_created"] = datetime.datetime.now()
    comment_json["last_edited"] = None

    # Get the user_id using the jwt identity.
    username = get_jwt_identity()
    query = db.select(User).filter_by(username=username)
    user = db.session.scalar(query)
    comment_json["user_id"] = user.id

    # Create the new entry.
    new_comment = Comment(**comment_json)

    # Add the entry to the comments table and commit changes.
    db.session.add(new_comment)
    db.session.commit()

    # Upon successful comment post, return the comment to the user.
    return jsonify(comment_schema.dump(new_comment))


# EDIT a comment by id
# /comments/<id>
@comments.route("/<int:comment_id>", methods=["PATCH"])
@jwt_required()
def update_comment_by_id(comment_id: int):
    '''
    This route will be used by either (a) a user to modify a comment they've made, or (b) an admin to modify a comment
    another user has made. The comment to be modified is specified by including the comment_id to the URL. The comment_id
    must be an integer and must have a corresponding entry in the comments table.

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The user modifying the comment must first be found in the database to check if they are an admin or to if their user id
    matches the user_id of the modified comment.
    Database statement: SELECT * FROM users WHERE username=get_jwt_identity().

    The comment being modified must also be found in the database, to firstly retrieve the user_id then to modify.
    Database statement: SELECT * FROM comments where id=comment_id;

    Example json body for POST request:
    {
        "comment": "string",
        "project_id": "integer"
    }

    JWT is required for this route. is_admin=True is required to modify a comment made by a different user.
    '''
    # Query the database to find the comment specified in the URL
    query = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(query)

    # If a comment with that id doesn't exist, provide feedback to the user of the error.
    response = comment_schema.dump(comment)
    if not response:
        return jsonify({"error": f"A comment with `id`={comment_id} does not exist in the database. No edits have been made."}), 404

    # Query the database to find the user making the modification.
    query = db.select(User).filter_by(username=get_jwt_identity())
    user = db.session.scalar(query)

    # Ensure that the user is either an admin or the owner of the comment.
    if not comment.user_id == user.id and not user.is_admin:
        return jsonify(error="You can only modify comments that you have made.")

    # Validate input coming from json request using schema.
    # Load-only fields need dummy data if not passed by the user.
    if request.json.get("comment"):
        response["comment"] = request.json["comment"]
    if request.json.get("project_id"):
        response["project_id"] = request.json["project_id"]
    else:
        response["project_id"] = 1
    # Add dummy user_id for schema valiation only
    response["user_id"] = 1
    # Add dummy datetime for schema validation only
    response["last_edited"] = datetime.datetime.now()
    response = comment_schema.load(response)

    # Map the json request properties to the comment if they are given.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("comment"):
        comment.comment = request.json["comment"]
        changed_string = " comment"
    if request.json.get("project_id"):
        comment.project_id = request.json["project_id"]
        changed_string += " project_id"
    comment.last_edited = datetime.datetime.now()

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No user information has been changed.")
    
    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following user information has been changed:{changed_string}.", **comment_schema.dump(comment))


# GET all comments
# /comments/
@comments.route("/", methods=["GET"])
@jwt_required()
def get_comments_list():
    '''
    This route is used to get a list of all the comments currently stored in the comments table.

    The following database query is used to get all entries in the comments table.
    Database statement: SELECT * FROM comments;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the comments table.
    query = db.select(Comment)
    comment_list = db.session.scalars(query)
    response = comments_schema.dump(comment_list)

    # Provide the user with a list of all comments.
    return jsonify(response)


# GET a comment by id
# /comments/<id>
@comments.route("/<int:comment_id>", methods=["GET"])
def get_comment_by_id(comment_id: int):
    '''
    This route will be used to retrieve details of a comment by providing the id of the comment in the URL. The id
    provided in the URL must be an integer and there must be a corresponding comment in the database.

    The following database query is used to find the entry with a matching id=comment_id.
    Database statement: SELECT * FROM comments WHERE id=comment_id;

    JWT is required for this route.
    '''
    # Query database to select the comment with a matching id=comment_id.
    query = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(query)
    response = comment_schema.dump(comment)

    # In the case that the comment_id is not matched, provide the user with the error feedback.
    if not response:
        return jsonify({"error": f"A comment with id=`{comment_id}` does not exist in the database."}), 404

    # Return the requested comment to the user.
    return jsonify(response)


# DELETE a comment by id
# /comments/delete_comment/<id>
@comments.route("/delete_comment/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_by_id(comment_id: int):
    '''
    This route will be used to delete a comment from the comments table based on the comment_id passed in the URL.
    A comment can only be deleted by either the original poster of the comment or an admin. The user_id of the comment
    must match the id of the user OR the user must have is_admin=True.

    The "/delete_comment/" portion was added to the URL to make it more deliberate and less prone to mistake. Deleting a
    comment has no flow-on effects to other tables.

    The user modifying the comment must first be found in the database to check if they are an admin or to if their user id
    matches the user_id of the modified comment.
    Database statement: SELECT * FROM users WHERE username=get_jwt_identity().

    The comment being modified must also be found in the database, to firstly retrieve the user_id then to modify.
    Database statement: SELECT * FROM comments where id=comment_id;

    JWT and is_admin=True are required for this route.
    '''
    # Query the database to find the comment specified in the URL
    query = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(query)

    # If a comment with that id doesn't exist, provide feedback to the user of the error.
    response = comment_schema.dump(comment)
    if not response:
        return jsonify({"error": f"A comment with `id`={comment_id} does not exist in the database. No edits have been made."}), 404

    # Query the database to find the user making the deletion.
    query = db.select(User).filter_by(username=get_jwt_identity())
    user = db.session.scalar(query)

    # Ensure that the user is either an admin or the owner of the comment.
    if not comment.user_id == user.id and not user.is_admin:
        return jsonify(error="You can only delete comments that you have made.")
    
    # Delete the entry and commit changes.
    db.session.delete(comment)
    db.session.commit()

    # Provide confirmation of the successful deletion to the user.
    return jsonify({
        "message": f"The comment with id=`{comment_id}` has been deleted successfully."
    })