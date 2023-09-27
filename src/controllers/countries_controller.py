from flask import Blueprint, jsonify, abort, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.countries import Country
from schemas.country_schema import country_schema, countries_schema
from controllers.auths_controller import check_admin

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
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@countries.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@countries.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a country
# /countries/
@countries.route("/", methods=["POST"])
@jwt_required()
def create_country():
    '''
    This route is used to create a country entry in the countries table. 

    The following statement will be used to create the entry in the countries data table.
    Database statement: INSERT INTO countries (country) VALUES (request.json["country"])

    Example json body for POST request:
    {
        "country": "string between 4 and 56 chars"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Extract the properties from the json request and create a new entry in countries table.
    country_json = country_schema.load(request.json)
    new_country = Country(**country_json)
    db.session.add(new_country)
    db.session.commit()

    # Return new created entry and 201 status
    return jsonify(country_schema.dump(new_country)), 201


# UPDATE a Country by ID
# /countries/<id>
@countries.route("/<int:country_id>", methods=["PUT"])
@jwt_required()
def update_country_by_id(country_id: int):
    '''
    This route is used to update a country in the countries table. This should be rarely used, and only used in the instance
    of correcting a misspelled country name or renaming a country. 

    Given that there is only one column (exluding id) in the countries table, a PUT request seemed as equally appropriate as a
    PATCH request. PUT has been used in this instance.

    The following statement will be used to filter the countries table to the specified entry based on id.
    Database statement: SELECT * FROM countries WHERE id=country_id;

    Example json body for PUT request:
    {
        "country": "string between 4 and 56 chars"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the matching entry in the countries table with id=country_id.
    query = db.select(Country).filter_by(id=country_id)
    country = db.session.scalar(query)
    response = country_schema.dump(country)

    if response:
        country_json = country_schema.load(request.json)

        # Map json request to country
        country.country = country_json["country"]

        # Commit changes
        db.session.commit()
        return jsonify(country_schema.dump(country))

    return jsonify({"error": f"A country with `id`={country_id} does not exist in the database. No updates have been made."}), 404


# GET all Countries
# /countries/
@countries.route("/", methods=["GET"])
@jwt_required()
def get_countries_list():
    '''
    This route is used to get a list of all country entries in the countries table.

    The following database query is used to get all entries in the countries table.
    Database statement: SELECT * FROM countries;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the countries table.
    query = db.select(Country)
    country_list = db.session.scalars(query)
    response = countries_schema.dump(country_list)

    return jsonify(response)


# GET a country by id
# /countries/<id>
@countries.route("/<int:country_id>", methods=["GET"])
@jwt_required()
def get_country_by_id(country_id: int):
    '''
    This route is used to get a specific entry from the countries table by providing the country_id in the URL.

    The following database query is used to find the entry with a matching id=country_id.
    Database statement: SELECT * FROM countries WHERE id=country_id;

    JWT is required for this route.
    '''
    query = db.select(Country).filter_by(id=country_id)
    country = db.session.scalar(query)
    response = country_schema.dump(country)

    if not response:
        return jsonify({"error": f"A country with id=`{country_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a country by id
# /countries/delete_country/<id>
@countries.route("/delete_country/<int:country_id>", methods=["DELETE"])
@jwt_required()
def delete_country_by_id(country_id: int):
    '''
    This route will be used to delete a country entry from the countries table based on the country id passed in the URL.

    The "/delete_country/" portion was added to the URL to make it more deliberate and less prone to mistake. Deleting a
    country would have significant flow-on effects to others tables and should be avoided.

    The following database query is used to select the country with the matching id=country_id.
    Database statement: SELECT * FROM countries WHERE id=country_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the matching country entry.
    country = Country.query.filter_by(id=country_id).first()
    response = country_schema.dump(country)

    # Provide feedback if that id does not exist in the countries table.
    if not response:
        return jsonify({"error": f"A country with `id`={country_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the entry and commit changes
    db.session.delete(country)
    db.session.commit()

    # Provide confirmation that the deletion was successful.
    return jsonify(message=f"The country with id=`{country_id}` has been deleted successfully.")
