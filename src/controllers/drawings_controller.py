from flask import Blueprint, jsonify, abort, request
import datetime

from main import db
from models.drawings import Drawing
from schemas.drawing_schema import drawing_schema, drawings_schema

drawings = Blueprint('drawing', __name__, url_prefix="/drawings")


# CREATE a drawing
# /drawings/
@drawings.route("/", methods=["POST"])
def create_drawing():
    '''
    
    '''
    drawing_json = drawing_schema.load(request.json)
    drawing_json["last_modified"] = datetime.datetime.now()
    new_drawing = Drawing(**drawing_json)

    db.session.add(new_drawing)
    db.session.commit()

    return jsonify(drawing_schema.dump(new_drawing))


# UPDATE a drawing by id
# /drawings/<id>
@drawings.route("/<int:drawing_id>", methods=["PUT"])
def update_drawing_by_id(drawing_id: int):
    '''
    
    '''
    query = db.select(Drawing).filter_by(id=drawing_id)
    drawing = db.session.scalar(query)
    response = drawing_schema.dump(drawing)

    if response:
        drawing_json = drawing_schema.load(request.json)

        # Map request json to drawing
        drawing.drawing_number = drawing_json["drawing_number"]
        drawing.project_id = drawing_json["project_id"]
        drawing.part_description = drawing_json.get("part_description")
        drawing.version = drawing_json.get("version")
        drawing.last_modified = datetime.datetime.now()

        # Commit changes
        db.session.commit()
        return jsonify(drawing_schema.dump(drawing))

    return abort(404, description=f"A drawing with `id`={drawing_id} does not exist in the database. No updates have been made.")


# GET all drawings
# /drawings/
@drawings.route("/", methods=["GET"])
def get_drawings_list():
    '''
    
    '''
    query = db.select(Drawing)
    drawing_list = db.session.scalars(query)
    response = drawings_schema.dump(drawing_list)

    return jsonify(response)


# GET a drawing by id
# /drawings/<id>
@drawings.route("/<int:drawing_id>", methods=["GET"])
def get_drawing_by_id(drawing_id: int):
    '''
    
    '''
    query = db.select(Drawing).filter_by(id=drawing_id)
    drawing = db.session.scalar(query)
    response = drawing_schema.dump(drawing)

    if not response:
        return abort(404, description=f"A drawing with id=`{drawing_id}` does not exist in the database.")

    return jsonify(response)


# DELETE a drawing by id
# /drawings/<id>
@drawings.route("/<int:drawing_id>", methods=["DELETE"])
def delete_drawing_by_id(drawing_id: int):
    '''
    
    '''
    drawing = Drawing.query.filter_by(id=drawing_id).first()
    response = drawing_schema.dump(drawing)

    if not response:
        return abort(404, description=f"A drawing with `id`={drawing_id} does not exist in the database. No deletions have been made.")

    db.session.delete(drawing)
    db.session.commit()

    return jsonify({
        "message": f"The drawing with id=`{drawing_id}` has been deleted successfully."
    })