from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required
import datetime

from main import db
from models.drawings import Drawing
from schemas.drawing_schema import drawing_schema, drawings_schema
from controllers.auths_controller import check_admin

drawings = Blueprint('drawing', __name__, url_prefix="/drawings")

# Error handlers
@drawings.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@drawings.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@drawings.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@drawings.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@drawings.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a drawing
# /drawings/
@drawings.route("/", methods=["POST"])
def create_drawing():
    '''
    This route is used to create a drawing entry in the drawings table. The drawing needs to be associated to a particular
    project.

    The following statement will be used to create the entry in the drawings data table.
    Database statement: INSERT INTO drawings (drawing_number, part_description, version, last_modified, project_id) 
    VALUES (request.json["drawing_number"], request.json["part_description"], request.json["version"], 
    datetime.datetime.now(), request.json["project_id"]);

    Example json body for POST request:
    {
        "drawing_number": "string, length from 3 to 10 chars",
        "part_description": "OPTIONAL, string",
        "version": "OPTIONAL, integer",
        "project_id": "integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Extract the properties from the json body and map to a new entry. 
    drawing_json = drawing_schema.load(request.json)
    drawing_json["last_modified"] = datetime.datetime.now()
    new_drawing = Drawing(**drawing_json)

    # Insert the new entry into the drawings table
    db.session.add(new_drawing)
    db.session.commit()

    # Return the new drawing entry to the user upon successful insertion
    return jsonify(drawing_schema.dump(new_drawing))


# UPDATE a drawing by id
# /drawings/<id>
@drawings.route("/<int:drawing_id>", methods=["PATCH"])
@jwt_required()
def update_drawing_by_id(drawing_id: int):
    '''
    This route will be used to update the details of a specified drawing. The drawing to be updated will be specified by
    including the drawing_id in the URL, where the drawing_id will be the id of an entry in the drawings table. Updated
    information is passed to this route via json body in the patch request.

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The following database query will filter the drawings.id column to match the drawings_id passed in the URL.
    Database statement: SELECT * FROM drawings WHERE id=drawing_id;

    Example json body for PATCH request:
    {
        "drawing_number": "OPTIONAL, string, length from 3 to 10 chars",
        "part_description": "OPTIONAL, string",
        "version": "OPTIONAL, integer",
        "project_id": "OPTIONAL, integer"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the matching drawing with id=drawing_id.
    query = db.select(Drawing).filter_by(id=drawing_id)
    drawing = db.session.scalar(query)
    response = drawing_schema.dump(drawing)

    # Return an error if the specified drawing does not exist in the drawings table.
    if not response:
        return jsonify({"error": f"A drawing with id=`{drawing_id}` does not exist in the database."}), 404

    # Validate input coming from json request using schema.
    # Load-only fields need dummy data if not passed in the request json
    if request.json.get("drawing_number"):
        response["drawing_number"] = request.json["drawing_number"]
    if request.json.get("part_description"):
        response["part_description"] = request.json["part_description"]
    if request.json.get("version"):
        response["version"] = request.json["version"]
    if request.json.get("project_id"):
        response["project_id"] = request.json["project_id"]
    else:
        response["project_id"] = 1
    response = drawing_schema.load(response)

    # Map the json request body to the entry selected by the database query.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("drawing_number"):
        drawing.drawing_number = request.json["drawing_number"]
        changed_string = " drawing_number"
    if request.json.get("part_description"):
        drawing.part_description = request.json["part_description"]
        changed_string += " part_description"
    if request.json.get("version"):
        drawing.version = request.json["version"]
        changed_string += " version"
    if request.json.get("project_id"):
        drawing.project_id = request.json["project_id"]
        changed_string += " project_id"

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No drawing information has been changed.") 

    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following drawing information has been changed:{changed_string}.", **drawing_schema.dump(drawing))


# GET all drawings
# /drawings/
@drawings.route("/", methods=["GET"])
@jwt_required()
def get_drawings_list():
    '''
    This route will be used to get a list of all drawings currently recorded in the drawings table.

    The following database query is used to get all entries in the drawings table.
    Database statement: SELECT * FROM drawings;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the drawings table. Dump into the plural schema.
    query = db.select(Drawing)
    drawing_list = db.session.scalars(query)
    response = drawings_schema.dump(drawing_list)

    # Return list of all drawings and their details.
    return jsonify(response)


# GET a drawing by id
# /drawings/<id>
@drawings.route("/<int:drawing_id>", methods=["GET"])
@jwt_required()
def get_drawing_by_id(drawing_id: int):
    '''
    This route is used to retrieve information about a specific drawing. The drawing is specified by entering the drawing_id
    in the URL. The drawing_id is then matched to the id of an entry in the drawings table. The drawing_id entered in the URL
    must be an integer and the corresponding entry in the drawings table must exist.

    The following query is used to select the unique entry in the projects table with a matching id=project_id.
    Database statement: SELECT * FROM drawings WHERE id=drawing_id;

    JWT is required for this route.
    '''
    # Query the database the find the entry in the drawings table with id=drawing_id.
    query = db.select(Drawing).filter_by(id=drawing_id)
    drawing = db.session.scalar(query)
    response = drawing_schema.dump(drawing)

    # If no such entry with specified id exists, provide feedback to user of the error.
    if not response:
        return jsonify({"error": f"A drawing with id=`{drawing_id}` does not exist in the database."}), 404

    # When successfully retrieving an entry, display drawing details to user.
    return jsonify(response)


# DELETE a drawing by id
# /drawings/delete_drawing/<id>
@drawings.route("/delete_drawing/<int:drawing_id>", methods=["DELETE"])
@jwt_required()
def delete_drawing_by_id(drawing_id: int):
    '''
    This route will be used by an admin to remove a drawing from the drawings table. To specify the drawings to be deleted,
    the drawing_id must be passed in the URL. The drawing_id must be an integer and a corresponding entry with matching id
    must exist in the drawing table.

    The "/delete_drawing/" portion of the URL was added to make sure that this action was deliberate and less prone to mistake.
    No flow on effects to other tables will occur, however, deletion of data must be carefully considered.

    The following data query will return the drawing with the matching drawing_id passed in the URL.
    Database statement: SELECT * FROM drawings WHERE id=drawing_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the entry in the drawings table with matching id=drawing_id.
    drawing = Drawing.query.filter_by(id=drawing_id).first()
    response = drawing_schema.dump(drawing)

    # If the specified drawing_id does not match an id, provide feedback of the error to the user.
    if not response:
        return jsonify({"error": f"A drawing with `id`={drawing_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the matching entry and commit changes.
    db.session.delete(drawing)
    db.session.commit()

    # Provide confirmation of successful deletion to the user.
    return jsonify({
        "message": f"The drawing with id=`{drawing_id}` has been deleted successfully."
    })