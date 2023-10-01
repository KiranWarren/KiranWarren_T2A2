from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.locations import Location
from models.manufactures import Manufacture
from schemas.location_schema import location_schema, locations_schema
from schemas.manufacture_schema import manufactures_schema
from controllers.auths_controller import check_admin

locations = Blueprint('location', __name__, url_prefix="/locations")

# Error handlers
@locations.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@locations.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@locations.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@locations.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@locations.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a location
# /locations/
@locations.route("/", methods=["POST"])
@jwt_required()
def create_location():
    '''
    This route is used to add a location entry to the locations table.

    The following statement will be used to create the entry in the locations data table.
    Database statement: INSERT INTO locations (name, admin_phone_number, country_id, location_type_id) 
    VALUES (location_json["name"], location_json["admin_phone_number"], location_json["country_id"],
    location_json["location_type_id"]);

    Example json body for POST request:
    {
        "name": "string"
        "admin_phone_number": "string containing numbers, spaces, '+'",
        "country_id": "integer"
        "location_type_id": "integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Extract json from request and load into schema. Map to a new entry in locations table.    
    location_json = location_schema.load(request.json)
    new_location = Location(**location_json)

    # Insert the entry and commit.
    db.session.add(new_location)
    db.session.commit()

    # Return the new entry as confirmation.
    return jsonify(location_schema.dump(new_location)), 201


# UPDATE a location by id
# /locations/<id>
@locations.route("/<int:location_id>", methods=["PATCH"])
@jwt_required()
def update_location_by_id(location_id: int):
    '''
    This route will be used by an admin to update the attributes of a location entry in the locations table.

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The following database query will filter the locations.id column to match the location id passed in the URL.
    Database statement: SELECT * FROM users WHERE id=location_id;

    Example json body for PATCH request:
    {
        "name": "OPTIONAL, string"
        "admin_phone_number": "OPTIONAL, string containing numbers, spaces, '+'",
        "country_id": "OPTIONAL, integer"
        "location_type_id": "OPTIONAL, integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Query the database to find the entry with matching id=location_id.
    query = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(query)
    response = location_schema.dump(location)

    # Return error response to user if no location exists with id=location_id.
    if not response:
        return jsonify({"error": f"A location with id=`{location_id}` does not exist in the database."}), 404

    # Validate input coming from json request using schema.
    # Load-only fields need dummy data if not passed by the user.
    if request.json.get("name"):
        response["name"] = request.json["name"]
    if request.json.get("admin_phone_number"):
        response["admin_phone_number"] = request.json["admin_phone_number"]
    if request.json.get("country_id"):
        response["country_id"] = request.json["country_id"]
    else:
        response["country_id"] = 1
    if request.json.get("location_type_id"):
        response["location_type_id"] = request.json["location_type_id"]
    else:
        response["location_type_id"] = 1
    response = location_schema.load(response)

    # Map the json request properties to the user if they are given.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("name"):
        location.name = request.json["name"]
        changed_string = " name"
    if request.json.get("admin_phone_number"):
        location.admin_phone_number = request.json["admin_phone_number"]
        changed_string += " admin_phone_number"
    if request.json.get("country_id"):
        location.country_id = request.json["country_id"]
        changed_string += " country_id"
    if request.json.get("location_type_id"):
        location.location_type_id = request.json["location_type_id"]
        changed_string += " location_type_id"

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No location information has been changed.")

    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following location information has been changed:{changed_string}.", **location_schema.dump(location))


# GET all locations
# /locations/
@locations.route("/", methods=["GET"])
@jwt_required()
def get_locations_list():
    '''
    This route is used to get a list of all location entries in the locations table.

    The following database query is used to get all entries in the locations table.
    Database statement: SELECT * FROM locations;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the locations table.
    query = db.select(Location)
    location_list = db.session.scalars(query)
    response = locations_schema.dump(location_list)

    return jsonify(response)


# GET a location by id
# /locations/<id>
@locations.route("/<int:location_id>", methods=["GET"])
@jwt_required()
def get_location_by_id(location_id: int):
    '''
    This route is used to find a specific location based on the location id provided in the URL. The location id passed 
    in the URL must be an integer and must exist in the locations table.

    The following database query will return the location with the matching location id passed in the URL.
    Database statement: SELECT * FROM locations WHERE id=location_id;

    JWT is required for this route.
    '''
    # Query the database to find the entry in the locations table with id=location_id.
    query = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(query)
    response = location_schema.dump(location)

    # If no such location exists in the table, provide feedback to user.
    if not response:
        return jsonify({"error": f"A location with id=`{location_id}` does not exist in the database."}), 404

    # Successful retrieval gives information of the requested location.
    return jsonify(response)


# DELETE a location by id
# /locations/delete_location/<id>
@locations.route("/delete_location/<int:location_id>", methods=["DELETE"])
@jwt_required()
def delete_location_by_id(location_id: int):
    '''
    This route will be used by an admin to remove a location entry from the locations table. The location to be removed
    will have an id matching the location_id passed in the URL. The location id passed by the admin must be an integer
    and must exist in the database.

    The "/delete_location/" portion of the URL was added to make sure that this action was deliberate and less prone to mistake.
    Accidentally deleting a location would have significant flow on effects to multiple tables and should be avoided.

    The following data query will return the location with the matching location_id passed in the URL.
    Database statement: SELECT * FROM locations WHERE id=location_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Query the database to find the entry in the locations table with a matching id=location_id.
    location = Location.query.filter_by(id=location_id).first()
    response = location_schema.dump(location)

    # If the given location_id doesn't exist, provide feedback to the user.
    if not response:
        return jsonify({"error": f"A location with `id`={location_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the entry and commit changes.
    db.session.delete(location)
    db.session.commit()

    # Provide confirmation to the user.
    return jsonify({
        "message": f"The location with id=`{location_id}` has been deleted successfully."
    })


# GET all manufacture offerings by location ID
# /locations/<id>/catalogue
@locations.route("/<int:location_id>/catalogue", methods=["GET"])
@jwt_required()
def get_location_catalogue(location_id: int):
    '''
    This route will be used to find all project manufacturing offerings a location provides; in other words, a catalogue for
    a specified location. The user gives the id of the desired location in the URL, which will be used to query the 
    manufactures table by location_id. Firstly, the locations table must be queried to ensure that a location with the given
    id exists in the locations table.

    The following database query will return the unique entry in the locations table with matching id to the location_id
    passed in the URL.
    Database statement: SELECT * FROM locations WHERE id=location_id;

    The following database query will return all entries in the manufactures table with location_id matching the location_id
    passed in the URL.
    Database statement: SELECT * FROM locations WHERE location_id=location_id;

    JWT is required for this route.
    '''
    # First ensure that a location with the provided location_id exists in the locations table.
    query = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(query)
    response = location_schema.dump(location)

    # In the case that such a location does not exist, provide feedback to the user of the error.
    if not response:
        return jsonify(error=f"A location with id=`{location_id}` does not exist in the database."), 404

    # Query the database to find all manufacturing offerings with the matching location_id.
    query = db.select(Manufacture).filter_by(location_id=location_id)
    manufactures_list = db.session.scalars(query)
    response = manufactures_schema.dump(manufactures_list)

    # In the case that this location does not have any manufacturing offerings listed, provide feedback.
    if not response:
        return jsonify(message=f"This location does not offer to manufacture any projects."), 200

    # Return the location's catalogue.
    return jsonify(response)