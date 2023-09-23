from flask import Blueprint, jsonify

from main import db
from models.countries import Country
from schemas.country_schema import country_schema, countries_schema

countries = Blueprint('country', __name__, url_prefix="/countries")

@countries.route("/", methods=["GET"])
def get_countries_list():
    query = db.select(Country)
    country_list = db.session.scalars(query)
    response = countries_schema.dump(country_list)

    return jsonify(response)