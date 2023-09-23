from flask import Blueprint, jsonify, abort, request

from main import db
from models.locations import Location
from schemas.location_schema import location_schema, locations_schema

locations = Blueprint('location', __name__, url_prefix="/locations")


# CREATE a location
# /locations/
@locations.route("/", methods=["POST"])
def create_location():
    '''
    
    '''
    location_json = location_schema.load(request.json)
    new_location = Location(**location_json)

    db.session.add(new_location)
    db.session.commit()

    return jsonify(location_schema.dump(new_location))


# UPDATE a location by id
# /locations/<id>
@locations.route("/<int:location_id>", methods=["PUT"])
def update_location_by_id(location_id: int):
    '''
    
    '''
    query = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(query)
    response = location_schema.dump(location)

    if response:
        location_json = location_schema.load(request.json)

        # Map request json to location
        location.name = location_json["name"]
        location.admin_phone_number = location_json["admin_phone_number"]
        location.country_id = location_json["country_id"]
        location.location_type_id = location_json["location_type_id"]

        # Commit changes
        db.session.commit()
        return jsonify(location_schema.dump(location))

    return abort(404, description=f"A location with `id`={location_id} does not exist in the database. No updates have been made.")


# GET all locations
# /locations/
@locations.route("/", methods=["GET"])
def get_locations_list():
    '''
    
    '''
    query = db.select(Location)
    location_list = db.session.scalars(query)
    response = locations_schema.dump(location_list)

    return jsonify(response)


# GET a location by id
# /locations/<id>
@locations.route("/<int:location_id>", methods=["GET"])
def get_location_by_id(location_id: int):
    '''
    
    '''
    query = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(query)
    response = location_schema.dump(location)

    if not response:
        return abort(404, description=f"A location with id=`{location_id}` does not exist in the database.")

    return jsonify(response)


# DELETE a location by id
# /locations/<id>
@locations.route("/<int:location_id>", methods=["DELETE"])
def delete_location_by_id(location_id: int):
    '''
    
    '''
    location = Location.query.filter_by(id=location_id).first()
    response = location_schema.dump(location)

    if not response:
        return abort(404, description=f"A location with `id`={location_id} does not exist in the database. No deletions have been made.")

    db.session.delete(location)
    db.session.commit()

    return jsonify({
        "message": f"The location with id=`{location_id}` has been deleted successfully."
    })