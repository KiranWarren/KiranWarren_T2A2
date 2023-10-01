from flask import Blueprint, jsonify, request, abort
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import jwt_required

from main import db
from models.currencies import Currency
from schemas.currency_schema import currency_schema, currencies_schema
from controllers.auths_controller import check_admin

currencies = Blueprint('currency', __name__, url_prefix="/currencies")

# Error handlers
@currencies.errorhandler(BadRequest)
def bad_request_error_handler(e):
    return jsonify({"error": e.description}), 400

@currencies.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify(e.messages), 400

@currencies.errorhandler(KeyError)
def key_error_error_handler(e):
    return jsonify({"key_error": f"The field `{e}` is required."}), 400

@currencies.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"integrity_error": f"{e}"}), 400

@currencies.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"data_error": f"{e}"}), 400


# CREATE a currency
# /currencies/
@currencies.route("/", methods=["POST"])
@jwt_required()
def create_currency():
    '''
    This route is used to create a currency entry in the currencies table. 

    The following statement will be used to create the entry in the countries data table.
    Database statement: INSERT INTO currencies (currency) VALUES (request.json["currency"])

    Example json body for POST request:
    {
        "currency_abbr": "string, must be length=3 and all capital letters"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Extract the information passed in the json body and map to a new entry.
    currency_json = currency_schema.load(request.json)
    new_currency = Currency(**currency_json)

    # Insert the new entry into the currencies table and commit changes.
    db.session.add(new_currency)
    db.session.commit()

    # Display the new entry for a successful insert
    return jsonify(currency_schema.dump(new_currency)), 201


# UPDATE a currency by id
# /currencies/<id>
@currencies.route("/<int:currency_id>", methods=["PUT"])
@jwt_required()
def update_currency_by_id(currency_id: int):
    '''
    This route is used to update a currency in the currencies table. This should be rarely used, and only used in the instance
    of correcting a misspelled currency abbreviation. A currency abbreviation is only 3 characters long, but sillier things have
    happened. 

    Given that there is only one column (exluding id) in the currencies table, a PUT request seemed as equally appropriate as a
    PATCH request. PUT has been used in this instance.

    The following statement will be used to filter the countries table to the specified entry based on id.
    Database statement: SELECT * FROM countries WHERE id=currency_id;

    Example json body for PUT request:
    {
        "currency_abbr": "string, must be length=3 and all capital letters"
    }

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401

    # Query the database to find the entry in the currencies table with matching id=currency_id.
    query = db.select(Currency).filter_by(id=currency_id)
    currency = db.session.scalar(query)
    response = currency_schema.dump(currency)

    # If the entry exists, proceed with the update.
    if response:
        currency_json = currency_schema.load(request.json)

        # Map request json to currency
        currency.currency_abbr = currency_json["currency_abbr"]

        # Commit changes
        db.session.commit()
        return jsonify(currency_schema.dump(currency))

    # If the entry with the given currency_id does not exist, provide feedback to the user.
    return jsonify({"error": f"A currency with `id`={currency_id} does not exist in the database. No updates have been made."}), 404


# GET all currencies
# /currencies/
@currencies.route("/", methods=["GET"])
@jwt_required()
def get_currencies_list():
    '''
    This route is used to get a list of all currency entries in the currencies table.

    The following database query is used to get all entries in the currencies table.
    Database statement: SELECT * FROM currencies;

    JWT is required for this route.
    '''
    # Query the database to select all entries in the currencies table.
    query = db.select(Currency)
    currency_list = db.session.scalars(query)
    response = currencies_schema.dump(currency_list)

    # Return all currencies.
    return jsonify(response)


# GET a currency by id
# /currencies/<id>
@currencies.route("/<int:currency_id>", methods=["GET"])
@jwt_required()
def get_currency_by_id(currency_id: int):
    '''
    This route is used to get a specific entry from the currencies table by providing the currency_id in the URL.

    The following database query is used to find the entry with a matching id=currency_id.
    Database statement: SELECT * FROM currencies WHERE id=currency_id;

    JWT is required for this route.    
    '''
    # Query the database to find the entry in the currencies table with matching id=currency_id.
    query = db.select(Currency).filter_by(id=currency_id)
    currency = db.session.scalar(query)
    response = currency_schema.dump(currency)

    # In the case that no entry with the given currency_id exists, provide feedback to the user.
    if not response:
        return jsonify({"error": f"A currency with id=`{currency_id}` does not exist in the database."}), 404

    # Provide the requested currency information.
    return jsonify(response)


# DELETE a currency by id
# /currencies/delete_currency/<id>
@currencies.route("/delete_currency/<int:currency_id>", methods=["DELETE"])
@jwt_required()
def delete_currency_by_id(currency_id: int):
    '''
    This route will be used to delete a currency entry from the currencies table based on the currency_id passed in the URL.

    The "/delete_currency/" portion was added to the URL to make it more deliberate and less prone to mistake. Deleting a
    currency would have flow-on effects to the manufactures table. All projects listed for manufacture with a price in the
    deleted currency will also be removed due to the cascade delete property.

    The following database query is used to select the currency with the matching id=currency_id.
    Database statement: SELECT * FROM currencies WHERE id=currency_id;

    JWT and is_admin=True are required for this route.
    '''
    # First call the check_admin function to check authorisation level.
    if not check_admin():
        return jsonify(message="Admin-level authorisation required for this function."), 401
    
    # Query the database to find the matching entry in the currencies table with id=currency_id.
    currency = Currency.query.filter_by(id=currency_id).first()
    response = currency_schema.dump(currency)

    # If there is no entry with matching id=currency_id, provide feedback to the user.
    if not response:
        return jsonify({"error": f"A currency with `id`={currency_id} does not exist in the database. No deletions have been made."}), 404

    # Delete the specified currency and commit changes.
    db.session.delete(currency)
    db.session.commit()

    # Provide feedback to the user of the successful deletion.
    return jsonify(message=f"The currency with id=`{currency_id}` has been deleted successfully.")