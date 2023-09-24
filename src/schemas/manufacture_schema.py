from marshmallow import fields

from main import ma

class ManufactureSchema(ma.Schema):

    # Validation
    location_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    price_estimate = fields.Float(required=True)
    currency_id = fields.Integer(required=True)

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

    project = fields.Nested("ProjectSchema", only=("id","title"))
    location = fields.Nested("LocationSchema", only=("name","country.country","admin_phone_number"))
    currency = fields.Nested("CurrencySchema", only=("currency_abbr",))

manufacture_schema = ManufactureSchema()
manufactures_schema = ManufactureSchema(many=True)