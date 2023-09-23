from flask import Blueprint, jsonify

from main import db
from models.location_types import LocationType
from schemas.location_type_schema import location_type_schema, location_types_schema

location_types = Blueprint('location_type', __name__, url_prefix="/location-types")

@location_types.route("/", methods=["GET"])
def get_location_types_list():
    query = db.select(LocationType)
    location_type_list = db.session.scalars(query)
    response = location_types_schema.dump(location_type_list)

    return jsonify(response)