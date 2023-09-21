from main import ma

class LocationSchema(ma.Schema):
    class Meta:
        fields = "id", "name", "admin_phone_number"

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)