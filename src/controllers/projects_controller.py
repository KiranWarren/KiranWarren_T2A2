from flask import Blueprint, jsonify, abort, request

from main import db
from models.projects import Project
from schemas.project_schema import project_schema, projects_schema

projects = Blueprint('project', __name__, url_prefix="/projects")


# CREATE a project
# /projects/
@projects.route("/", methods=["POST"])
def create_project():
    '''
    
    '''
    project_json = project_schema.load(request.json)
    new_project = Project(**project_json)

    db.session.add(new_project)
    db.session.commit()

    return jsonify(project_schema.dump(new_project))


# UPDATE a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["PUT"])
def update_project_by_id(project_id: int):
    '''
    
    '''
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    if response:
        project_json = project_schema.load(request.json)

        # Map request json to project
        project.title = project_json["title"]
        project.published_date = project_json.get("published_date")
        project.description = project_json.get("description")
        project.certification_number = project_json.get("certification_number")

        # Commit changes
        db.session.commit()
        return jsonify(project_schema.dump(project))

    return abort(404, description=f"A project with `id`={project_id} does not exist in the database. No updates have been made.")


# GET all projects
# /projects/
@projects.route("/", methods=["GET"])
def get_projects_list():
    '''
    
    '''
    query = db.select(Project)
    project_list = db.session.scalars(query)
    response = projects_schema.dump(project_list)

    return jsonify(response)


# GET a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["GET"])
def get_project_by_id(project_id: int):
    '''
    
    '''
    query = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(query)
    response = project_schema.dump(project)

    if not response:
        return abort(404, description=f"A project with id=`{project_id}` does not exist in the database.")

    return jsonify(response)


# DELETE a project by id
# /projects/<id>
@projects.route("/<int:project_id>", methods=["DELETE"])
def delete_project_by_id(project_id: int):
    '''
    
    '''
    project = Project.query.filter_by(id=project_id).first()
    response = project_schema.dump(project)

    if not response:
        return abort(404, description=f"A project with `id`={project_id} does not exist in the database. No deletions have been made.")

    db.session.delete(project)
    db.session.commit()

    return jsonify({
        "message": f"The project with id=`{project_id}` has been deleted successfully."
    })