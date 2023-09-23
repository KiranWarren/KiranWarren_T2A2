from flask import Blueprint, jsonify, abort, request

from main import db
from models.location_types import LocationType
from schemas.location_type_schema import location_type_schema, location_types_schema

location_types = Blueprint('location_type', __name__, url_prefix="/location-types")

# CREATE a location type
# /location-types/
@location_types.route("/", methods=["POST"])
def create_location_type():
    '''
    
    '''
    location_type_json = location_type_schema.load(request.json)
    new_location_type = LocationType(**location_type_json)

    db.session.add(new_location_type)
    db.session.commit()

    return jsonify(location_type_schema.dump(new_location_type))


# UPDATE a location type by id
# /location-types/<id>
@location_types.route("/<int:location_type_id>", methods=["PUT"])
def update_location_type_by_id(location_type_id: int):
    '''
    
    '''
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

    return abort(404, description=f"A location_type with `id`={location_type_id} does not exist in the database. No updates have been made.")


# GET all location types
# /location-types/
@location_types.route("/", methods=["GET"])
def get_location_types_list():
    query = db.select(LocationType)
    location_type_list = db.session.scalars(query)
    response = location_types_schema.dump(location_type_list)

    return jsonify(response)


# DELETE a location type by id
# /location-types/<id>
@location_types.route("/<int:location_type_id>", methods=["DELETE"])
def delete_location_type_by_id(location_type_id: int):
    '''
    
    '''
    location_type = LocationType.query.filter_by(id=location_type_id).first()
    response = location_type_schema.dump(location_type)

    if not response:
        return abort(404, description=f"A location_type with `id`={location_type_id} does not exist in the database. No deletions have been made.")

    db.session.delete(location_type)
    db.session.commit()

    return jsonify({
        "message": f"The location_type with id=`{location_type_id}` has been deleted successfully."
    })