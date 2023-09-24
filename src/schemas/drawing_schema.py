from main import ma
from schemas.project_schema import ProjectSchema

class DrawingSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "drawing_number",
            "project_id",
            "part_description",
            "version",
            "last_modified",
            "project"
        )

        load_only = ["project_id"]

    project = ma.Nested(ProjectSchema)

drawing_schema = DrawingSchema()
drawings_schema = DrawingSchema(many=True)