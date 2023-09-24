from marshmallow.validate import Length, And, Regexp
from marshmallow import fields

from main import ma

class ProjectSchema(ma.Schema):

    # Validation
    title = fields.String(required=True, validate=Length(min=3, max=50))
    published_date = fields.Date(required=False)
    description = fields.String(required=False)
    certification_number = fields.String(required=False, validate=Length(min=3, max=25))
    
    class Meta:
        fields = (
            "id",
            "title", 
            "published_date",
            "description",
            "certification_number"
        )

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)