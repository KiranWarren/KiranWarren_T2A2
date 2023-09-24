from marshmallow.validate import Length
from marshmallow import fields

from main import ma

class DrawingSchema(ma.Schema):

    # Validation
    drawing_number = fields.String(required=True, validate=Length(min=3, max=10))
    part_description = fields.String(required=False)
    version = fields.Integer(required=False)
    project_id = fields.Integer(required=True)

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

    project = fields.Nested("ProjectSchema", only=("title","id"))

drawing_schema = DrawingSchema()
drawings_schema = DrawingSchema(many=True)