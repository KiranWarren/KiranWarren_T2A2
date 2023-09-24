from main import ma
from schemas.user_schema import UserSchema
from schemas.project_schema import ProjectSchema

class CommentSchema(ma.Schema):
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

    project = ma.Nested(ProjectSchema)
    user = ma.Nested(UserSchema)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)