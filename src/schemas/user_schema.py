from main import ma
from schemas.location_schema import LocationSchema

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id", 
            "username", 
            "email_address",
            "position",
            "is_admin",
            "location",
            "location_id"
        )

        load_only = ["location_id"]

    location = ma.Nested(LocationSchema)

user_schema = UserSchema()
users_schema = UserSchema(many=True)