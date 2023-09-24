from marshmallow.validate import Length, And, Regexp
from marshmallow import fields

from main import ma
from schemas.country_schema import CountrySchema
from schemas.location_type_schema import LocationTypeSchema

class LocationSchema(ma.Schema):

    # Validation
    name = fields.String(required=True, validate=Length(min=4, max=50))
    admin_phone_number = fields.String(required=True, validate=And(Length(min=8, max=25), Regexp('^[0123456789 +]+$')))
    country_id = fields.Integer(required=True)
    location_type_id = fields.Integer(required=True)

    class Meta:
        fields = (
            "id", 
            "name", 
            "admin_phone_number",
            "country",
            "location_type",
            "country_id",
            "location_type_id"
        )

        load_only = ["country_id", "location_type_id"]

    country = fields.Nested("CountrySchema", only=("country",))
    location_type = fields.Nested("LocationTypeSchema", only=("location_type",))

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)