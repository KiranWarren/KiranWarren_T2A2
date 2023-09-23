from main import ma
from schemas.country_schema import CountrySchema
from schemas.location_type_schema import LocationTypeSchema

class LocationSchema(ma.Schema):
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

    country = ma.Nested(CountrySchema)
    location_type = ma.Nested(LocationTypeSchema)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)