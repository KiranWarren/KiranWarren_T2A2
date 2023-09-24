from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models.manufactures import Manufacture
from schemas.manufacture_schema import manufacture_schema, manufactures_schema

manufactures = Blueprint('manufacture', __name__, url_prefix="/manufactures")

# Error handlers
@manufactures.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@manufactures.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@manufactures.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"error": f"The field `{e}` is required."}), 400

@manufactures.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400

@manufactures.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# CREATE a manufacture
# /manufactures/
@manufactures.route("/", methods=["POST"])
def create_manufacture():
    '''
    
    '''
    manufacture_json = manufacture_schema.load(request.json)
    manufacture_json["id"] = str(manufacture_json["location_id"]) + "-" + str(manufacture_json["project_id"])
    new_manufacture = Manufacture(**manufacture_json)

    db.session.add(new_manufacture)
    db.session.commit()

    return jsonify(manufacture_schema.dump(new_manufacture))


# UPDATE a manufacture by id
# /manufactures/<id>
@manufactures.route("/<string:manufacture_id>", methods=["PUT"])
def update_manufacture_by_id(manufacture_id: str):
    '''
    
    '''
    query = db.select(Manufacture).filter_by(id=manufacture_id)
    manufacture = db.session.scalar(query)
    response = manufacture_schema.dump(manufacture)

    if response:
        manufacture_json = manufacture_schema.load(request.json)

        # Map request json to manufacture
        manufacture.location_id = manufacture_json["location_id"]
        manufacture.project_id = manufacture_json["project_id"]
        manufacture.id = str(manufacture_json["location_id"]) + "-" + str(manufacture_json["project_id"])
        manufacture.price_estimate = manufacture_json["price_estimate"]
        manufacture.currency_id = manufacture_json["currency_id"]

        # Commit changes
        db.session.commit()
        return jsonify(manufacture_schema.dump(manufacture))

    return jsonify({"error": f"A manufacture with `id`={manufacture_id} does not exist in the database. No updates have been made."}), 404


# GET all manufactures
# /manufactures/
@manufactures.route("/", methods=["GET"])
def get_manufactures_list():
    '''
    
    '''
    query = db.select(Manufacture)
    manufacture_list = db.session.scalars(query)
    response = manufactures_schema.dump(manufacture_list)

    return jsonify(response)


# GET a manufacture by id
# /manufactures/<id>
@manufactures.route("/<string:manufacture_id>", methods=["GET"])
def get_manufacture_by_id(manufacture_id: str):
    '''
    
    '''
    query = db.select(Manufacture).filter_by(id=manufacture_id)
    manufacture = db.session.scalar(query)
    response = manufacture_schema.dump(manufacture)

    if not response:
        return jsonify({"error": f"A manufacture with id=`{manufacture_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a manufacture by id
# /manufactures/<id>
@manufactures.route("/<string:manufacture_id>", methods=["DELETE"])
def delete_manufacture_by_id(manufacture_id: str):
    '''
    
    '''
    manufacture = Manufacture.query.filter_by(id=manufacture_id).first()
    response = manufacture_schema.dump(manufacture)

    if not response:
        return jsonify({"error": f"A manufacture with `id`={manufacture_id} does not exist in the database. No deletions have been made."}), 404

    db.session.delete(manufacture)
    db.session.commit()

    return jsonify({
        "message": f"The manufacture with id=`{manufacture_id}` has been deleted successfully."
    })