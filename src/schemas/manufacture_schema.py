from main import ma
from schemas.project_schema import ProjectSchema
from schemas.location_schema import LocationSchema
from schemas.currency_schema import CurrencySchema

class ManufactureSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "location_id",
            "project_id",
            "price_estimate",
            "currency_id",
            "location",
            "project",
            "currency",
            "id"
        )

        load_only = ["project_id", "location_id", "currency_id"]

    project = ma.Nested(ProjectSchema)
    location = ma.Nested(LocationSchema)
    currency = ma.Nested(CurrencySchema)

manufacture_schema = ManufactureSchema()
manufactures_schema = ManufactureSchema(many=True)