from main import ma

class LocationSchema(ma.Schema):
    class Meta:
        fields = (
            "id", 
            "name", 
            "admin_phone_number",
            "country_id",
            "location_type_id"
        )

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)