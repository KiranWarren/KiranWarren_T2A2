from marshmallow.validate import Length
from marshmallow import fields

from main import ma

class LocationTypeSchema(ma.Schema):

    # Validation
    location_type = fields.String(required=True, validate=Length(min=4, max=25))

    class Meta:
        fields = (
            "id", 
            "location_type"
        )

location_type_schema = LocationTypeSchema()
location_types_schema = LocationTypeSchema(many=True)