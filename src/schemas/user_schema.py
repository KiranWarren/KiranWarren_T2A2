from marshmallow.validate import Length, And, Regexp
from marshmallow import fields

from main import ma

class UserSchema(ma.Schema):

    # Validation
    email_address = fields.Email(required=True)
    password = fields.String(validate=Length(min=6, max=50))
    username = fields.String(validate=And(Length(min=2, max=40), Regexp('^[a-z0-9]+$')))
    location_id = fields.Integer(required=True)
    position = fields.String(validate=Length(max=40))
    
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


class LoginSchema(ma.Schema):
    class Meta:
        fields = (
            "username",
            "password"
        )
        

user_schema = UserSchema()
users_schema = UserSchema(many=True)
login_schema = LoginSchema()