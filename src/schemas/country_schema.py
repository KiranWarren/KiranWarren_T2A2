from main import ma

class CountrySchema(ma.Schema):
    class Meta:
        fields = (
            "id", 
            "country"
        )

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)