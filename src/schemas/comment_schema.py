from marshmallow.validate import Length
from marshmallow import fields

from main import ma
from schemas.user_schema import UserSchema
from schemas.project_schema import ProjectSchema

class CommentSchema(ma.Schema):
    
    # Validation
    comment = fields.String(required=True, validate=Length(min=1))
    project_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)

    class Meta:
        fields = (
            "id",
            "comment",
            "when_created",
            "last_edited",
            "project_id",
            "user_id",
            "project",
            "user"
        )

        load_only = ["project_id", "user_id"]

    project = fields.Nested("ProjectSchema", only=("title",))
    user = fields.Nested("UserSchema", only=("username",))

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)