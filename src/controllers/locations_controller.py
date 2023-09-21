from flask import Blueprint, jsonify

from main import db
from models.locations import Location
from schemas.location_schema import location_schema, locations_schema

locations = Blueprint('location', __name__, url_prefix="/locations")

@locations.route("/", methods=["GET"])
def get_locations_list():
    query = db.select(Location)
    location_list = db.session.scalars(query)
    response = locations_schema.dump(location_list)

    return jsonify(response)