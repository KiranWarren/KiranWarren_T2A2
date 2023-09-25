from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required
import datetime

from main import db
from models.comments import Comment
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
def create_comment():
    '''
    
    '''
    comment_json = comment_schema.load(request.json)
    comment_json["when_created"] = datetime.datetime.now()
    comment_json["last_edited"] = None
    new_comment = Comment(**comment_json)

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment_schema.dump(new_comment))


# UPDATE a comment by id
# /comments/<id>
@comments.route("/<int:comment_id>", methods=["PUT"])
def update_comment_by_id(comment_id: int):
    '''
    
    '''
    query = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(query)
    response = comment_schema.dump(comment)

    if response:
        comment_json = comment_schema.load(request.json)

        # Map request json to comment
        comment.user_id = comment_json["user_id"]
        comment.project_id = comment_json["project_id"]
        comment.comment = comment_json.get("comment")
        comment.last_edited = datetime.datetime.now()

        # Commit changes
        db.session.commit()
        return jsonify(comment_schema.dump(comment))

    return jsonify({"error": f"A comment with `id`={comment_id} does not exist in the database. No updates have been made."}), 404


# GET all comments
# /comments/
@comments.route("/", methods=["GET"])
@jwt_required()
def get_comments_list():
    '''
    
    '''
    query = db.select(Comment)
    comment_list = db.session.scalars(query)
    response = comments_schema.dump(comment_list)

    return jsonify(response)


# GET a comment by id
# /comments/<id>
@comments.route("/<int:comment_id>", methods=["GET"])
def get_comment_by_id(comment_id: int):
    '''
    
    '''
    query = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(query)
    response = comment_schema.dump(comment)

    if not response:
        return jsonify({"error": f"A comment with id=`{comment_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a comment by id
# /comments/<id>
@comments.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment_by_id(comment_id: int):
    '''
    
    '''
    comment = Comment.query.filter_by(id=comment_id).first()
    response = comment_schema.dump(comment)

    if not response:
        return jsonify({"error": f"A comment with `id`={comment_id} does not exist in the database. No deletions have been made."}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        "message": f"The comment with id=`{comment_id}` has been deleted successfully."
    })