from main import ma

class ProjectSchema(ma.Schema):
    class Meta:
        fields = (
            "title", 
            "published_date",
            "description",
            "certification_number"
        )

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)