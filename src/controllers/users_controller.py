from flask import Blueprint, jsonify, abort, request

from main import db
from models.users import User
from schemas.user_schema import user_schema, users_schema

users = Blueprint('user', __name__, url_prefix="/users")


# CREATE a user
# /users/
@users.route("/", methods=["POST"])
def create_user():
    '''
    
    '''
    user_json = user_schema.load(request.json)
    new_user = User(**user_json)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))


# UPDATE a user by id
# /users/<id>
@users.route("/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id: int):
    '''
    
    '''
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    response = user_schema.dump(user)

    if response:
        user_json = user_schema.load(request.json)

        # Map request json to user
        user.username = user_json["username"]
        user.email_address = user_json["email_address"]
        user.is_admin = user_json["is_admin"]
        user.location_id = user_json["location_id"]
        user.position = user_json.get("position")

        # Commit changes
        db.session.commit()
        return jsonify(user_schema.dump(user))

    return abort(404, description=f"A user with `id`={user_id} does not exist in the database. No updates have been made.")


# GET all users
# /users/
@users.route("/", methods=["GET"])
def get_users_list():
    '''
    
    '''
    query = db.select(User)
    user_list = db.session.scalars(query)
    response = users_schema.dump(user_list)

    return jsonify(response)


# GET a user by id
# /users/<id>
@users.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    '''
    
    '''
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    response = user_schema.dump(user)

    if not response:
        return abort(404, description=f"A user with id=`{user_id}` does not exist in the database.")

    return jsonify(response)


# DELETE a user by id
# /users/<id>
@users.route("/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id: int):
    '''
    
    '''
    user = User.query.filter_by(id=user_id).first()
    response = user_schema.dump(user)

    if not response:
        return abort(404, description=f"A user with `id`={user_id} does not exist in the database. No deletions have been made.")

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": f"The user with id=`{user_id}` has been deleted successfully."
    })