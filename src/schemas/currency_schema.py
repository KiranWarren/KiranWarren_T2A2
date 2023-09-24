from marshmallow.validate import Length, And, Regexp
from marshmallow import fields

from main import ma

class CurrencySchema(ma.Schema):

    # Validation
    currency_abbr = fields.String(required=True, validate=And(Length(min=3, max=3), Regexp('^[A-Z]+$')))

    class Meta:
        fields = (
            "id", 
            "currency_abbr"
        )

currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)