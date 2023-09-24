from marshmallow.validate import Length, And, Regexp
from marshmallow import fields

from main import ma
from schemas.location_schema import LocationSchema

class UserSchema(ma.Schema):

    # Validation
    email_address = fields.Email(required=True)
    password = fields.String(validate=Length(min=6, max=25))
    username = fields.String(validate=And(Length(min=2, max=25), Regexp('^[a-z0-9]+$')))

    class Meta:
        fields = (
            "id", 
            "username", 
            "email_address",
            "position",
            "password",
            "is_admin",
            "location",
            "location_id"
        )

        load_only = ["location_id", "password"]

    location = fields.Nested("LocationSchema", only=("name","country.country"))

user_schema = UserSchema()
users_schema = UserSchema(many=True)