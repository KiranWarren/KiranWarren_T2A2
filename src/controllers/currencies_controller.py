from flask import Blueprint, jsonify, request, abort
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models.currencies import Currency
from schemas.currency_schema import currency_schema, currencies_schema

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
def create_currency():
    '''
    
    '''
    currency_json = currency_schema.load(request.json)
    new_currency = Currency(**currency_json)

    db.session.add(new_currency)
    db.session.commit()

    return jsonify(currency_schema.dump(new_currency))


# UPDATE a currency by id
# /currencies/<id>
@currencies.route("/<int:currency_id>", methods=["PUT"])
def update_currency_by_id(currency_id: int):
    '''
    
    '''
    query = db.select(Currency).filter_by(id=currency_id)
    currency = db.session.scalar(query)
    response = currency_schema.dump(currency)

    if response:
        currency_json = currency_schema.load(request.json)

        # Map request json to currency
        currency.currency_abbr = currency_json["currency_abbr"]

        # Commit changes
        db.session.commit()
        return jsonify(currency_schema.dump(currency))

    return jsonify({"error": f"A currency with `id`={currency_id} does not exist in the database. No updates have been made."}), 404


# GET all currencies
# /currencies/
@currencies.route("/", methods=["GET"])
def get_currencies_list():
    query = db.select(Currency)
    currency_list = db.session.scalars(query)
    response = currencies_schema.dump(currency_list)

    return jsonify(response)


# GET a currency by id
# /currencies/<id>
@currencies.route("/<int:currency_id>", methods=["GET"])
def get_currency_by_id(currency_id: int):
    '''
    
    '''
    query = db.select(Currency).filter_by(id=currency_id)
    currency = db.session.scalar(query)
    response = currency_schema.dump(currency)

    if not response:
        return jsonify({"error": f"A currency with id=`{currency_id}` does not exist in the database."}), 404

    return jsonify(response)


# DELETE a currency by id
# /currencies/<id>
@currencies.route("/<int:currency_id>", methods=["DELETE"])
def delete_currency_by_id(currency_id: int):
    '''
    
    '''
    currency = Currency.query.filter_by(id=currency_id).first()
    response = currency_schema.dump(currency)

    if not response:
        return jsonify({"error": f"A currency with `id`={currency_id} does not exist in the database. No deletions have been made."}), 404

    db.session.delete(currency)
    db.session.commit()

    return jsonify({
        "message": f"The currency with id=`{currency_id}` has been deleted successfully."
    })