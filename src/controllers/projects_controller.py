from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.projects import Project
from models.manufactures import Manufacture
from models.drawings import Drawing
from models.comments import Comment
from schemas.project_schema import project_schema, projects_schema
from schemas.manufacture_schema import manufactures_schema
from schemas.drawing_schema import drawings_schema
from schemas.comment_schema import comments_schema
from controllers.auths_controller import check_admin

projects = Blueprint('project', __name__, url_prefix="/projects")

# Error handlers
@projects.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@projects.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@projects.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@projects.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@projects.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a project
# /projects/
@projects.route("/", methods=["POST"])
@jwt_required()
def create_project():
    '''
    This route will be used for an admin to create a new entry in the projects table. The admin will pass information about
    the project in a json body via a post request to this URL.

    The following statement will be used to create the entry in the projects data table.
    Database statement: INSERT INTO projects (title, published_date, description, certification_number) 
    VALUES (request.json["title"], request.json["published_date"], request.json["description"], 
    request.json["certification_number"]);

    Example json body for POST request:
    {
        "title": "string, length from 3 to 50 chars"
        "published_date": "OPTIONAL, date",
        "description": "OPTIONAL, string",
        "certification_number": "OPTIONAL, string, length from 3 to 25"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Extract the properties from the json body and map to a new entry.
    project_json = project_schema.load(request.json)
    new_project = Project(**project_json)

    # Add the new entry into the projects table and commit changes.
    db.session.add(new_project)
    db.session.commit()

    # Return the details of the new project for a successful insert.
    return jsonify(project_schema.dump(new_project))


# UPDATE a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["PATCH"])
@jwt_required()
def update_project_by_id(project_id: int):
    '''
    The route will be used by an admin to update the details of an existing project entry in the projects table.

    For ease of use, the user only has to pass the fields that they want to update. The PATCH request feels more appropriate
    in this instance given that not all fields are required to be passed.

    The following database query will filter the projects.id column to match the project id passed in the URL.
    Database statement: SELECT * FROM projects WHERE id=project_id;

    Example json body for PATCH request:
    {
        "title": "OPTIONAL, string, length from 3 to 50 chars"
        "published_date": "OPTIONAL, date",
        "description": "OPTIONAL, string",
        "certification_number": "OPTIONAL, string, length from 3 to 25"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the entry in the projects table with the matching id=project_id.
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    # Return an error if the specified project does not exist in the projects table.
    if not response:
        return jsonify({"error": f"A project with id=`{project_id}` does not exist in the database."}), 404
    
    # Validate input coming from json request using schema.
    if request.json.get("title"):
        response["title"] = request.json["title"]
    if request.json.get("published_date"):
        response["published_date"] = request.json["published_date"]
    if request.json.get("description"):
        response["description"] = request.json["description"]
    if request.json.get("certification_number"):
        response["certification_number"] = request.json["certification_number"]
    response = project_schema.load(response)

    # Map the json request body to the entry selected by the database query.
    # Build string of changes to provide feedback to user.
    changed_string = ""
    if request.json.get("title"):
        project.title = request.json["title"]
        changed_string = " title"
    if request.json.get("published_date"):
        project.published_date = request.json["published_date"]
        changed_string += " published_date"
    if request.json.get("description"):
        project.description = request.json["description"]
        changed_string += " description"
    if request.json.get("certification_number"):
        project.certification_number = request.json["certification_number"]
        changed_string += " certification_number"

    # Check if any information was changed. Give response if nothing was changed.
    if changed_string == "":
        return jsonify(message="No project information has been changed.") 

    # Commit changes and return changed information.
    db.session.commit()
    return jsonify(message=f"The following project information has been changed:{changed_string}.", **project_schema.dump(project))


# GET all projects
# /projects/
@projects.route("/", methods=["GET"])
@jwt_required()
def get_projects_list():
    '''
    This route will be used by a user to get a list of all of the projects stored in the projects table.

    The following database query is used to get all entries in the projects table.
    Database statement: SELECT * FROM projects;

    JWT is required for this route.
    '''
    # Query the database to find all entries in the projects table
    query = db.select(Project)
    project_list = db.session.scalars(query)
    response = projects_schema.dump(project_list)

    return jsonify(response)


# GET a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project_by_id(project_id: int):
    '''
    This route is used to find a specific project based on the project_id pass in the URL. The id passed in the URL must be
    an integer, and the corresponding entry must exist in the projects table.

    The following query is used to select the unique entry in the projects table with a matching id=project_id.
    Database statement: SELECT * FROM projects WHERE id=project_id;

    JWT is required for this route.
    '''
    # Query the database to find the entry in the projects table with matching id=project_id.
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    # If no record with the given id exists, return the error to the user for feedback.
    if not response:
        return jsonify({"error": f"A project with id=`{project_id}` does not exist in the database."}), 404

    # Return the requested project information back to the user.
    return jsonify(response)


# DELETE a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project_by_id(project_id: int):
    '''
    This route will be used by an admin to remove a project entry from the projects table. The project to be deleted is
    specified by passing the project_id in the URL. The id passed in the URL must be an integer and the corresponding entry
    must exist in the projects table.

    The "/delete_project/" portion of the URL was added to make sure that this action was deliberate and less prone to mistake.
    Accidentally deleting a project would have significant flow on effects to multiple tables and should be avoided. It may be
    better to change the project description to "obsolete".

    The following data query will return the project with the matching project_id passed in the URL.
    Database statement: SELECT * FROM projects WHERE id=project_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the specified project.
    project = Project.query.filter_by(id=project_id).first()
    response = project_schema.dump(project)

    # If the project_id passed in the URL does not match an id in the projects table, provide the user with the error message.
    if not response:
        return jsonify({"error": f"A project with `id`={project_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the project entry and commit changes.
    db.session.delete(project)
    db.session.commit()

    # Upon successful deletion, provide user with confirmation.
    return jsonify({
        "message": f"The project with id=`{project_id}` has been deleted successfully."
    })


# GET all manufacturing offerings by project ID
# /projects/<id>/suppliers
@projects.route("/<int:project_id>/suppliers", methods=["GET"])
@jwt_required()
def get_project_suppliers(project_id: int):
    '''
    This route will be used by a user to find all the locations that offer to fabricate a specified project. If a user
    finds a project they need built in the projects list, they can enter that project id into this route to find
    which internal workshops will manufacture the project, and for what price.

    The following database query will return the unique entry in the projects table with matching id to the project_id
    passed in the URL.
    Database statement: SELECT * FROM projects WHERE id=projects_id;

    The following database query will return all entries in the manufactures table with project_id matching the project_id
    passed in the URL.
    Database statement: SELECT * FROM manufactures WHERE project_id=project_id;

    JWT is required for this route.
    '''
    # First ensure that a project with the provided project_id exists in the projects table.
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    # In the case that such a project does not exist, provide feedback to the user of the error.
    if not response:
        return jsonify(error=f"A project with id=`{project_id}` does not exist in the database."), 404

    # Query the database to find all manufacturing offerings with the matching project_id.
    query = db.select(Manufacture).filter_by(project_id=project_id)
    manufactures_list = db.session.scalars(query)
    response = manufactures_schema.dump(manufactures_list)

    # In the case that no locations offer to manufacture this project, notify the user instead of giving an empty response.
    if not response:
        return jsonify(message=f"No locations currently offer to manufacture this project."), 200

    # Return the list of suppliers and their prices.
    return jsonify(response)


# GET all drawings by project ID
# /projects/<id>/drawings
@projects.route("/<int:project_id>/drawings", methods=["GET"])
@jwt_required()
def get_project_drawings(project_id: int):
    '''
    This route will be used by a user to retrieve all of the drawing numbers required to build a specified project. It is 
    common for someone to want to get a local third party to manufacture a project instead of an internal location. There 
    may also be no internal locations that offer to manufacture a particular project. This route allows the user to retrieve
    all drawings for a project so that they can be requested from engineering.

    The following database query will return the unique entry in the projects table with matching id to the project_id
    passed in the URL.
    Database statement: SELECT * FROM projects WHERE id=projects_id;

    The following database query will return all entries in the drawings table with project_id matching the project_id
    passed in the URL.
    Database statement: SELECT * FROM drawings WHERE project_id=project_id;

    JWT is required for this route.
    '''
    # First ensure that a project with the provided project_id exists in the projects table.
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    # In the case that such a project does not exist, provide feedback to the user of the error.
    if not response:
        return jsonify(error=f"A project with id=`{project_id}` does not exist in the database."), 404

    # Query the database to find all drawings with the matching project_id.
    query = db.select(Drawing).filter_by(project_id=project_id)
    drawings_list = db.session.scalars(query)
    response = drawings_schema.dump(drawings_list)

    # In the case that no drawings have been linked to the specified project, provide feedback to the user.
    if not response:
        return jsonify(message=f"No drawings have yet been linked to the requested project."), 200

    # Return the list of drawings for the specified project.
    return jsonify(response)


# GET all comments by project ID
# /projects/<id>/comments
@projects.route("/<int:project_id>/comments", methods=["GET"])
@jwt_required()
def get_project_comments(project_id: int):
    '''
    This route will be used by a user to retrieve all of the comments made by users on a specified project. A user may
    want to see discussion regarding a particular project. The user must specify which project they would like to see
    discussion on by providing the project_id in the URL. The project_id must be an integer and a project with the
    corresponding id must exist in the projects table.

    The following database query will return the unique entry in the projects table with matching id to the project_id
    passed in the URL.
    Database statement: SELECT * FROM projects WHERE id=projects_id;

    The following database query will return all entries in the comments table with project_id matching the project_id
    passed in the URL.
    Database statement: SELECT * FROM comments WHERE project_id=project_id;

    JWT is required for this route.
    '''
    # First ensure that a project with the provided project_id exists in the projects table.
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    # In the case that such a project does not exist, provide feedback to the user of the error.
    if not response:
        return jsonify(error=f"A project with id=`{project_id}` does not exist in the database."), 404

    # Query the database to find all comments with the matching project_id.
    query = db.select(Comment).filter_by(project_id=project_id)
    comments_list = db.session.scalars(query)
    response = comments_schema.dump(comments_list)

    # In the case that there is no discussion of a project, provide feedback to the user.
    if not response:
        return jsonify(message=f"No comments have yet been posted about this project."), 200

    # Return the list of comments for the specified project.
    return jsonify(response)