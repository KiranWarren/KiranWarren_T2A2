from main import ma

class CurrencySchema(ma.Schema):
    class Meta:
        fields = (
            "id", 
            "currency_abbr"
        )

currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)