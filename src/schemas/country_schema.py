from marshmallow.validate import Length
from marshmallow import fields

from main import ma

class CountrySchema(ma.Schema):

    # Validation
    country = fields.String(required=True, validate=Length(min=4, max=56))

    class Meta:
        fields = (
            "id", 
            "country"
        )

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)