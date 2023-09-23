from flask import Blueprint, jsonify

from main import db
from models.currencies import Currency
from schemas.currency_schema import currency_schema, currencies_schema

currencies = Blueprint('currency', __name__, url_prefix="/currencies")

@currencies.route("/", methods=["GET"])
def get_currencies_list():
    query = db.select(Currency)
    currency_list = db.session.scalars(query)
    response = currencies_schema.dump(currency_list)

    return jsonify(response)