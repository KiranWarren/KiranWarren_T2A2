from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models.countries import Country
from schemas.country_schema import country_schema, countries_schema

countries = Blueprint('country', __name__, url_prefix="/countries")

# Error handlers
@countries.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@countries.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@countries.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"error": f"The field `{e}` is required."}), 400

@countries.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400

@countries.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# CREATE a country
# /countries/
@countries.route("/", methods=["POST"])
def create_country():
    '''
    
    '''
    country_json = country_schema.load(request.json)
    new_country = Country(**country_json)

    db.session.add(new_country)
    db.session.commit()

    return jsonify(country_schema.dump(new_country))


# UPDATE a country by id
# /countries/<id>
@countries.route("/<int:country_id>", methods=["PUT"])
def update_country_by_id(country_id: int):
    '''
    
    '''
    query = db.select(Country).filter_by(id=country_id)
    country = db.session.scalar(query)
    response = country_schema.dump(country)

    if response:
        country_json = country_schema.load(request.json)

        # Map request json to country
        country.country = country_json["country"]

        # Commit changes
        db.session.commit()
        return jsonify(country_schema.dump(country))

    return jsonify({"error": f"A country with `id`={country_id} does not exist in the database. No updates have been made."}), 404


# GET all countries
# /countries/
@countries.route("/", methods=["GET"])
def get_countries_list():
    query = db.select(Country)
    country_list = db.session.scalars(query)
    response = countries_schema.dump(country_list)

    return jsonify(response)


# GET a country by id
# /countries/<id>
@countries.route("/<int:country_id>", methods=["GET"])
def get_country_by_id(country_id: int):
    '''
    
    '''
    query = db.select(Country).filter_by(id=country_id)
    country = db.session.scalar(query)
    response = country_schema.dump(country)

    if not response:
        return jsonify({"error": f"A country with id=`{country_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a country by id
# /countries/<id>
@countries.route("/<int:country_id>", methods=["DELETE"])
def delete_country_by_id(country_id: int):
    '''
    
    '''
    country = Country.query.filter_by(id=country_id).first()
    response = country_schema.dump(country)

    if not response:
        return jsonify({"error": f"A country with `id`={country_id} does not exist in the database. No deletions have been made."}), 404

    db.session.delete(country)
    db.session.commit()

    return jsonify({
        "message": f"The country with id=`{country_id}` has been deleted successfully."
    })