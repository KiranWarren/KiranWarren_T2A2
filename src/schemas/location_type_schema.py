from main import ma

class LocationTypeSchema(ma.Schema):
    class Meta:
        fields = (
            "id", 
            "location_type"
        )

location_type_schema = LocationTypeSchema()
location_types_schema = LocationTypeSchema(many=True)