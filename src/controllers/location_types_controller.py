from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.location_types import LocationType
from schemas.location_type_schema import location_type_schema, location_types_schema
from controllers.auths_controller import check_admin

location_types = Blueprint('location_type', __name__, url_prefix="/location-types")

# Error handlers
@location_types.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@location_types.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@location_types.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@location_types.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@location_types.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a location type
# /location-types/
@location_types.route("/", methods=["POST"])
@jwt_required()
def create_location_type():
    '''
    This route is used to add a location_type entry to the location_types table.

    The following statement will be used to create the entry in the location_types data table.
    Database statement: INSERT INTO location_types (location_type) VALUES (request.json["location_type"])

    Example json body for POST request:
    {
        "location_type": "string"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Extract json from request and load into schema. Map to a new entry in location_types table.
    location_type_json = location_type_schema.load(request.json)
    new_location_type = LocationType(**location_type_json)

    # Add entry and commit changes.
    db.session.add(new_location_type)
    db.session.commit()

    # Return the new entry for confirmation.
    return jsonify(location_type_schema.dump(new_location_type))


# UPDATE a location type by id
# /location-types/<id>
@location_types.route("/<int:location_type_id>", methods=["PUT"])
@jwt_required()
def update_location_type_by_id(location_type_id: int):
    '''
    This route is used to update a location type in the location_types table. This should be rarely used, and only used 
    in the instance of correcting a misspelled location type name.

    Given that there is only one column (exluding id) in the location_types table, a PUT request seemed as equally 
    appropriate as a PATCH request. PUT has been used in this instance.

    The following statement will be used to filter the location_types table to the specified entry based on id.
    Database statement: SELECT * FROM location_types WHERE id=location_type_id;

    Example json body for PUT request:
    {
        "location_type": "string"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Find the matching location type entry in the database with id=location_type_id.
    query = db.select(LocationType).filter_by(id=location_type_id)
    location_type = db.session.scalar(query)
    response = location_type_schema.dump(location_type)

    if response:
        location_type_json = location_type_schema.load(request.json)

        # Map request json to location_type
        location_type.location_type = location_type_json["location_type"]

        # Commit changes
        db.session.commit()
        return jsonify(location_type_schema.dump(location_type))

    return jsonify({"error": f"A location_type with `id`={location_type_id} does not exist in the database. No updates have been made."}), 404


# GET all location types
# /location-types/
@location_types.route("/", methods=["GET"])
@jwt_required()
def get_location_types_list():
    '''
    This route is used to get a list of all location type entries in the location_types table.

    The following database query is used to get all entries in the location_types table.
    Database statement: SELECT * FROM location_types;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the location_types table.
    query = db.select(LocationType)
    location_type_list = db.session.scalars(query)
    response = location_types_schema.dump(location_type_list)

    return jsonify(response)


# GET a location type by id
# /location-types/<id>
@location_types.route("/<int:location_type_id>", methods=["GET"])
@jwt_required()
def get_location_type_by_id(location_type_id: int):
    '''
    This route is used to get a specific entry from the location_types table by providing the location_type_id in the URL.

    The following database query is used to find the entry with a matching id=location_type_id.
    Database statement: SELECT * FROM countries WHERE id=country_id;

    JWT is required for this route.
    '''
    # Query the database to find a matching entry in the location_types table where id=location_type_id.
    query = db.select(LocationType).filter_by(id=location_type_id)
    location_type = db.session.scalar(query)
    response = location_type_schema.dump(location_type)

    if not response:
        return jsonify({"error": f"A location_type with id=`{location_type_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a location type by id
# /location-types/delete_loc_type/<id>
@location_types.route("/delete_loc_type/<int:location_type_id>", methods=["DELETE"])
@jwt_required()
def delete_location_type_by_id(location_type_id: int):
    '''
    This route will be used to delete a location type entry from the location_types table based on the country id passed 
    in the URL.

    The "/delete_loc_type/" portion was added to the URL to make it more deliberate and less prone to mistake. Deleting a
    location type would have significant flow-on effects to others tables and should be avoided.

    The following database query is used to select the location type with the matching id=location_type_id.
    Database statement: SELECT * FROM location_types WHERE id=location_type_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find a matching entry in the location_types table where id=location_type_id.
    location_type = LocationType.query.filter_by(id=location_type_id).first()
    response = location_type_schema.dump(location_type)

    if not response:
        return jsonify({"error": f"A location_type with `id`={location_type_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the entry and commit the changes.
    db.session.delete(location_type)
    db.session.commit()

    return jsonify({
        "message": f"The location_type with id=`{location_type_id}` has been deleted successfully."
    })