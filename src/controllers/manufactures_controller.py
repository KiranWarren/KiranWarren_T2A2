from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.manufactures import Manufacture
from schemas.manufacture_schema import manufacture_schema, manufactures_schema
from controllers.auths_controller import check_admin

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
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@manufactures.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@manufactures.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a manufacture
# /manufactures/
@manufactures.route("/", methods=["POST"])
@jwt_required()
def create_manufacture():
    '''
    This route is used to create a manufacturing offering. A manufacturing offering is an instance of a location offering
    to fabricate a project for an estimated price. By adding manufacturing offering entries to the data table, a catalogue
    of all internal fabrication can be constructed and maintained.

    The following statement will be used to create the entry in the manufactures data table.
    Database statement: INSERT INTO manufactures (location_id, project_id, price_estimate, currency_id) 
    VALUES (request.json["location_id"], request.json["project_id"], request.json["price_estimate"], 
    request.json["currency_id"]);

    Example json body for POST request:
    {
        "location_id": "integer",
        "project_id": "integer",
        "price_estimate": "float",
        "currency_id": "integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Extract the properties from the request json and map to a new entry
    manufacture_json = manufacture_schema.load(request.json)
    new_manufacture = Manufacture(**manufacture_json)

    # Insert the new entry into the manufactures table and commit changes.
    db.session.add(new_manufacture)
    db.session.commit()

    # Upon successful insertion, provide feedback to the user by displaying the new entry.
    return jsonify(manufacture_schema.dump(new_manufacture))


# UPDATE a manufacture by ids
# /manufactures/loc/<id1>/proj/<id2>
@manufactures.route("/loc/<int:location_id>/proj/<int:project_id>", methods=["PATCH"])
@jwt_required()
def update_manufacture_by_ids(location_id: int, project_id: int):
    '''
    This route is used by an admin to update the details of a manufacture offering. In most cases, this will be to update
    the price estimate contained in the entry. Alternatively, this may be used to correct the location, project or
    currency id if a wrong value had been accidentally entered.

    To specify a particular manufacture entry, the ids of the entry must be given in the URL. The location id is given first,
    after the "/loc/" section. The project id is given next, after the "/proj/" section of the URL. For example, to update
    the manufacturing offering at location 2 & project 6, the URL must be "/manufactures/loc/2/proj/6".

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The following database query will filter the manufactures table to find the location and project ids requested.
    Database statement: SELECT * FROM manufactures WHERE location_id=location_id AND project_id=project_id;

    Example json body for PATCH request:
    {
        "location_id": "OPTIONAL, integer"
        "project_id": "OPTIONAL, float",
        "price_estimate": "OPTIONAL, integer",
        "currency_id": "OPTIONAL, integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Query the manufactures table with conditions on two columns: location_id and project_id. These foreign keys combine
    # to create the composite key for the table, so the result should always be unique.
    query = db.select(Manufacture).filter_by(
        location_id=location_id,
        project_id=project_id
        )
    manufacture = db.session.scalar(query)
    response = manufacture_schema.dump(manufacture)

    # If no such entry exists in the manufactures table, provide feedback of the error to the user.
    if not response:
        return jsonify(error=f"A manufacturing offering with location_id=`{location_id}` and project_id=`{project_id}` does not exist in the database."), 404
    
    # Validate input coming from json request using schema.
    # Load-only fields must be given placeholder data if not passed by the user.
    if request.json.get("location_id"):
        response["location_id"] = request.json["location_id"]
    else:
        response["location_id"] = 1
    if request.json.get("project_id"):
        response["project_id"] = request.json["project_id"]
    else:
        response["project_id"] = 1
    if request.json.get("price_esimate"):
        response["price_esimate"] = request.json["price_esimate"]
    if request.json.get("currency_id"):
        response["currency_id"] = request.json["currency_id"]
    else:
        response["currency_id"] = 1
    response = manufacture_schema.load(response)

    # Map the json request body to the entry selected by the database query.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("location_id"):
        manufacture.location_id = request.json["location_id"]
        changed_string = " location_id"
    if request.json.get("project_id"):
        manufacture.project_id = request.json["project_id"]
        changed_string += " project_id"
    if request.json.get("price_estimate"):
        manufacture.price_estimate = request.json["price_estimate"]
        changed_string += " price_estimate"
    if request.json.get("currency_id"):
        manufacture.currency_id = request.json["currency_id"]
        changed_string += " currency_id"

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No manufacture offering information has been changed.") 

    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following manufacture offering information has been changed:{changed_string}.", **manufacture_schema.dump(manufacture))


# GET all manufactures
# /manufactures/
@manufactures.route("/", methods=["GET"])
@jwt_required()
def get_complete_catalogue():
    '''
    This route will be used to retrieve all entries in the manufactures table. The information retrieved will be the full
    catalogue of internal fabrication, not filtered by either location or project.

    The following database query is used to get all entries in the projects table.
    Database statement: SELECT * FROM manufactures;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the manufactures table.
    query = db.select(Manufacture)
    manufacture_list = db.session.scalars(query)
    response = manufactures_schema.dump(manufacture_list)

    # Return all entries to the user in json format.
    return jsonify(response)


# GET a manufacture by ids
# /manufactures/loc/<id1>/proj/<id2>
@manufactures.route("/loc/<int:location_id>/proj/<int:project_id>", methods=["GET"])
@jwt_required()
def get_manufacture_by_ids(location_id: int, project_id: int):
    '''
    This route will be used to retrieve the details of a specific item in the catalogue, narrowed down by the particular project
    that is to be fabricated and the location that offers to fabricate it. 

    To specify a particular manufacture entry, the ids of the entry must be given in the URL. The location id is given first,
    after the "/loc/" section. The project id is given next, after the "/proj/" section of the URL. For example, to update
    the manufacturing offering at location 2 & project 6, the URL must be "/manufactures/loc/2/proj/6".

    The following database query will filter the manufactures table to find the location and project ids requested.
    Database statement: SELECT * FROM manufactures WHERE location_id=location_id AND project_id=project_id;

    JWT is required for this route.
    '''
    # Query the manufactures table with conditions on two columns: location_id and project_id. These foreign keys combine
    # to create the composite key for the table, so the result should always be unique.
    query = db.select(Manufacture).filter_by(
        location_id=location_id,
        project_id=project_id
        )
    manufacture = db.session.scalar(query)
    response = manufacture_schema.dump(manufacture)

    # If no such entry exists in the manufactures table, provide feedback of the error to the user.
    if not response:
        return jsonify(error=f"A manufacturing offering with location_id=`{location_id}` and project_id=`{project_id}` does not exist in the database."), 404
    
    # Return the specified manufactures entry in json format.
    return jsonify(response)


# DELETE a manufacture by ids
# /manufactures/loc/<id1>/proj/<id2>
@manufactures.route("/loc/<int:location_id>/proj/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_manufacture_by_ids(location_id: int, project_id: int):
    '''
    This route will be used by an admin to delete an entry from the manufactures table. If a location no longer offers to 
    fabricate a particular project for some reason, the corresponding entry in the catalogue can be removed.

    To specify a particular manufacture entry, the ids of the entry must be given in the URL. The location id is given first,
    after the "/loc/" section. The project id is given next, after the "/proj/" section of the URL. For example, to update
    the manufacturing offering at location 2 & project 6, the URL must be "/manufactures/loc/2/proj/6".

    The following database query will filter the manufactures table to find the location and project ids requested.
    Database statement: SELECT * FROM manufactures WHERE location_id=location_id AND project_id=project_id;

    JWT and is_admin=True are required for this route.
    '''
    # Query the manufactures table with conditions on two columns: location_id and project_id. These foreign keys combine
    # to create the composite key for the table, so the result should always be unique.
    query = db.select(Manufacture).filter_by(
        location_id=location_id,
        project_id=project_id
        )
    manufacture = db.session.scalar(query)
    response = manufacture_schema.dump(manufacture)

    # If no such entry exists in the manufactures table, provide feedback of the error to the user.
    if not response:
        return jsonify(error=f"A manufacturing offering with location_id=`{location_id}` and project_id=`{project_id}` does not exist in the database."), 404
    
    # Before deleting, get some details that can be later used to give feedback to the user.
    loc = manufacture.location.name
    proj = manufacture.project.title

    # Delete the specified record and commit changes.
    db.session.delete(manufacture)
    db.session.commit()

    # Upon successful deletion, provide confirmation to the user.
    return jsonify(message=f"The following manufacturing offering has been removed from the catalogue: {loc} (id={location_id}) fabricating project {proj} (id={project_id}).")